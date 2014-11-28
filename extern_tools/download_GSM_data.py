import argparse
import imaplib
import time
from configparser import ConfigParser
from datetime import timedelta, datetime
import email
import re
import os
import getpass
import zipfile
import shutil
from multiprocessing.dummy import Pool as ThreadPool, Queue
from multiprocessing import Pool as ProcessPool
import sys

# Parameters
config = ConfigParser()
config.read('gsm_config.ini')
mail_folder = config.defaults()['mail_folder']
mail_passwd = config.defaults()['mail_passwd']
mail_server = config.defaults()['mail_server']
mail_user = config.defaults()['mail_user']
username = getpass.getuser()
ptt_pattern = re.compile('[0]*(?P<platform>[0-9]+)g')
dest_path = os.path.join(os.path.expanduser('~%s' % username), "Desktop", 'import_gsm_' + datetime.today().strftime('%Y-%m-%d'))

# Maximum number of concurrent connections
max_connections = 8

# Globals
connection_queue = Queue()

def initialize_connections():
   """Create a connection to the mailbox server and add it to the Queue."""
   try:
      cn = imaplib.IMAP4_SSL(mail_server)
      cn.login(mail_user, mail_passwd)
      cn.select(mail_folder)
      connection_queue.put(cn)
   except:
      pass

def fetch_zip_file(gsm):
   full_filename = None
   try:
      # Acquire a connection
      client = connection_queue.get()
      # The sort command does not work with Outlook, use search instead and sort by uid.
      result, data = client.uid(
            'search', 
            '(FROM {sender} SUBJECT {subject})'.format(sender = 'gsm.emailer@microwavetelemetry.net', subject = 'ID#' + format(gsm, '08d')))
      uid_list = data[0].split()
      if len(uid_list) > 0:
         uid = uid_list[-1]
         print('Downloading last e-mail for transmitter : {0}'.format(gsm))
         result, data = client.uid('fetch', uid, 'RFC822')
         text = data[0][1]
         msg = email.message_from_bytes(text)
         for part in msg.walk():
            if part.get_content_type() == 'application/zip':
               filename = part.get_filename()
               data = part.get_payload(decode=True)
               full_filename = os.path.join(dest_path, filename)
               f = open(full_filename, 'wb')
               f.write(data)
               f.close()
               break
   except Exception as e:
       print('Error occurs when processing transmitter : {0}'.format(gsm))
   finally:
       connection_queue.put(client)
       return full_filename

def readGSMDataFile(fileName):
   gsm_list = []
   with open(fileName) as f:
       gsm_list = [int(line) for line in f.readlines()]
   return gsm_list

def unzip(zipFilePath):
   if zipFilePath is not None:
      zfile = zipfile.ZipFile(zipFilePath)

      for name in zfile.namelist():
         dirName, filename = os.path.split(name)
         _, file_extension = os.path.splitext(filename)

         if file_extension != '.kml' and filename != '':
            # GPS file
            if ptt_pattern.search(filename) is not None:
                fd = open(os.path.join(dest_path, 'gps', filename), 'wb')
            # Eng file
            else:
                fd = open(os.path.join(dest_path, 'eng', filename), 'wb')
            fd.write(zfile.read(name))
            fd.close()
      zfile.close()

def fetch_and_extract(gsm_list):
   start = time.time()
   tmp_pathData = os.path.join(os.path.expanduser('~%s' % username), "AppData", "Local", "Temp", "GSM_extractData")
   
   # Max imap concurrent connections for Office365 : 20
   thread_pool = ThreadPool(max_connections, initialize_connections)
   zip_files = thread_pool.map_async(fetch_zip_file, gsm_list).get()
   
   # Close connections
   while not connection_queue.empty():
      cn = connection_queue.get()
      cn.close()
      cn.logout()
   
   # Extracting csv files from .zip
   print('Extracting files ...')
   process_pool = ProcessPool()
   process_pool.map(unzip, zip_files)

   print('Downloads and extraction successfully completed in {0}'.format(timedelta(seconds = time.time() - start)))
   
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    # Create directory
    try:
        os.mkdir(dest_path)
    except FileExistsError:
        action = input('Directory ' + dest_path + ' already exists. Would you like to delete it (y/n) ? ')
        if action == 'y':
            shutil.rmtree(dest_path)
            os.mkdir(dest_path)
        else:
            sys.exit(0)

    os.mkdir(os.path.join(dest_path, 'gps'))
    os.mkdir(os.path.join(dest_path, 'eng'))
    gsm_list = readGSMDataFile(args.filename)
    fetch_and_extract(gsm_list)