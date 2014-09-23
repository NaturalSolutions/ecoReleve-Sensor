import imaplib
import time
from datetime import timedelta, datetime
import email
import re
import os
import getpass
import zipfile
import shutil
from Tkinter import *
from gsm_config import *
from multiprocessing.dummy import Pool as ThreadPool, Queue
from multiprocessing import Pool as ProcessPool
from traceback import print_exc

# Parameters
username = getpass.getuser()
tmp_path = os.path.join(os.path.expanduser('~%s' % username), "AppData", "Local", "Temp", "SatData-Africa")

# Maximum number of concurrent connections
max_connections = 8

# Globals
connection_queue = Queue()

# Lambdas
str2datetime = lambda s: datetime.strptime(s, '%Y-%m-%d')

def initialize_connections():
   """Create a connection to the mailbox server and add it to the Queue."""
   try:
      cn = imaplib.IMAP4_SSL(mail_server)
      cn.login(mail_user, mail_passwd)
      cn.select(mail_folder)
      connection_queue.put(cn)
   except:
      pass

def fetch_zip_file(args):
   full_filename = None
   try:
      ptt, d = args
      # Acquire a connection
      client = connection_queue.get()
      # The sort command does not work with Outlook, use search instead and sort by uid.
      result, data = client.uid(
            'search', 
            '(SENTSINCE {date} FROM {sender} SUBJECT {subject})'.format(date = d, sender = 'gsm.emailer@microwavetelemetry.net', subject = 'ID#' + format(int(ptt), '08d')))
      uid_list = data[0].split()
      if len(uid_list) > 0:
         uid = uid_list[-1]
         print('Downloading last e-mail for transmitter : {0}'.format(ptt))
         result, data = client.uid('fetch', uid, 'RFC822')
         text = data[0][1]
         msg = email.message_from_string(text)
         for part in msg.walk():
            if part.get_content_type() == 'application/zip':
               filename = part.get_filename()
               data = part.get_payload(decode=True)
               full_filename = os.path.join(tmp_path, filename)
               f = open(full_filename, 'wb')
               f.write(data)
               f.close()
               break
   except:
      print('Error occurs when processing transmitter : {0}'.format(ptt))
   finally:
      connection_queue.put(client)
      return full_filename

def readGSMDataFile(fileName):
   dict = {}
   with open(fileName) as f:
      for line in f.readlines():
         gsmData = line.split()
         dict[gsmData[0].strip()] = str2datetime(gsmData[1].strip())
   return dict

def unzip(zipFilePath):
   if zipFilePath is not None:
      destDir = os.path.dirname(zipFilePath)
      zfile = zipfile.ZipFile(zipFilePath)

      for name in zfile.namelist():
         dirName, filename = os.path.split(name)
         _, file_extension = os.path.splitext(filename)
         fullDirName = os.path.join(destDir, dirName)

         if filename == '':
            # directory
            newDir = os.path.join(destDir, dirName)
            if not os.path.exists(newDir):
               os.mkdir(newDir)
         elif file_extension != '.kml':
            # file
            fd = open(os.path.join(destDir, name), 'wb')
            fd.write(zfile.read(name))
            fd.close()
      zfile.close()

#nombre_de_jours => nb de jours ou les mails sont extrait
#duree_max => nb de jours pour lesquels les donnees des transmetteurs seront pris en compte
def gogogo(dict_of_ptt, nombre_de_jours = 7, duree_max = 2):
   start = time.time()
   tmp_pathData = os.path.join(os.path.expanduser('~%s' % username), "AppData", "Local", "Temp", "GSM_extractData")
   
   ptt_pattern = re.compile('ID#[0]*(?P<ptt>[0-9]+)_')
   
   # Cleaning previous imports #
   print "Deleting old data files"
   if os.path.exists(tmp_pathData):
      shutil.rmtree(tmp_pathData)
   os.mkdir(tmp_pathData)
   
   if os.path.exists(tmp_path):
      shutil.rmtree(tmp_path)
   os.mkdir(tmp_path)

   print "Working directory : %s" % tmp_path

   d = (datetime.today() - timedelta(nombre_de_jours)).strftime("%d-%b-%Y")
   gsmStartDateDefault = (datetime.today() - timedelta(7)).strftime("%Y-%m-%d")
   
   # Max imap concurrent connections for Office365 : 20
   thread_pool = ThreadPool(max_connections, initialize_connections)
   zip_files = thread_pool.map_async(fetch_zip_file, [(ptt, d) for ptt in dict_of_ptt.keys()]).get()
   
   print('Extracting files ...')
   
   process_pool = ProcessPool()
   process_pool.map(unzip, zip_files)

   while not connection_queue.empty():
      cn = connection_queue.get()
      cn.close()
      cn.logout()

   print('Downloads and extraction successfully completed in {0}'.format(timedelta(seconds = time.time() - start)))

   print "Creating output files"
   e_f = open(os.path.join(tmp_pathData, 'GSM_Microwave_Engineering_%s.txt' % datetime.today().strftime("%Y%m%d")),'w+')
   g_f =open(os.path.join(tmp_pathData, 'GSM_Microwave_GPS_%s.txt' % datetime.today().strftime("%Y%m%d")),'w+')

   print_header_e = True
   print_header_g = True
   
   for (dir_path, dir_names, filenames) in os.walk(tmp_path):
      if dir_path == tmp_path:
         continue
      if not filenames:
         continue

      (_, GSM_ID) = os.path.split(dir_path)
      print 'GSM_ID : ', GSM_ID
      iGSMid = str(int(GSM_ID))
      if iGSMid in dict_of_ptt.keys():
         for name in filenames:
            short_name, fileExtension = os.path.splitext(name)

            if fileExtension != ".txt":
               continue
            ##Get the file date
            (_, fileDate) = short_name.split('_')


            pattern1 = re.compile("%se_" % GSM_ID)
            pattern2 = re.compile("%sg_" % GSM_ID)
            fd = open(os.path.join(dir_path, name), 'r')
            lines = fd.readlines();
            fd.close()

            dlimitMin = dict_of_ptt[iGSMid] 
            dlimitMax = dlimitMin+ timedelta(days=duree_max+1)  
            # Fichier Engineering
            if pattern1.search(short_name):
               if print_header_e:
                  e_f.write(lines[0].strip() + "\tGSM_ID\tfile_date\n")
                  print_header_e = False
               for line in reversed(lines[1:]):
                  try:
                     (date, _, _) = line.strip().partition(' ')
                     date = str2datetime(date)
                     if date < dlimitMin:
                        break
                     elif date < dlimitMax:
                        e_f.write(line.strip() + "\t" + GSM_ID + "\t" + fileDate +"\n")
                  except:
                     pass
            # Fichier GPS
            elif pattern2.search(short_name):
               if print_header_g:
                  g_f.write(lines[0].strip() + "\tGSM_ID\tfile_date\n")
                  print_header_g = False
               for line in reversed(lines[1:]):
                  try:
                     (date, _, _) = line.strip().partition(' ')
                     date = str2datetime(date)
                     if date < dlimitMin:
                        break
                     elif date < dlimitMax:
                        g_f.write(line.strip() + "\t" + GSM_ID + "\t" + fileDate +"\n")
                  except:
                     pass

   print "Deleting temporary files"
   shutil.rmtree(tmp_path)

   e_f.close()
   g_f.close()

class Application(Frame):
   def getGSMData(self):
      try: 
         print "run script"
         nombre_de_jours = int(self.nbjours.get())
         duree_max = int(self.dureemax.get()) 
         if mode == 'test':
            dict_of_ptt = readGSMDataFile('GSMdata_test.txt')
         else:
            dict_of_ptt = readGSMDataFile('GSMdata.txt')
         gogogo(dict_of_ptt, nombre_de_jours, duree_max)
         print "------------------------DONE--------------------"

      except ValueError:
         print Error

   def createWidgets(self):
      self.lb = {}
      self.lb['nbjours'] = Label(self, text="Get mail for X days")
      self.lb['dureemax'] = Label(self, text="Get data for X days")
      self.nbjours = Entry(self)
      self.dureemax = Entry(self)
      self.nbjours.insert(0, 7)
      self.dureemax.insert(0, 2)
      
      self.lb['nbjours'].pack({"side": "left"})
      
      self.nbjours.pack({"side": "left"})
      self.lb['dureemax'].pack({"side": "left"})
      self.dureemax.pack({"side": "left"})

      self.startScript = Button(self)
      self.startScript["text"] = "GetData",
      self.startScript["command"] = self.getGSMData
      self.startScript.pack({"side": "left"})

      self.QUIT = Button(self)
      self.QUIT["text"] = "QUIT"
      self.QUIT["fg"]   = "red"
      self.QUIT["command"] =  self.quit

      self.QUIT.pack({"side": "left"})
      
   def __init__(self, master=None):
      Frame.__init__(self, master)
      self.pack()
      self.createWidgets()

if __name__ == '__main__':
   root = Tk()
   app = Application(master=root)
   app.mainloop()
   root.destroy()