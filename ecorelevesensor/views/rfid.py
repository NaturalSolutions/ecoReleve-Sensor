"""
Created on Thu Aug 28 16:45:25 2014

@author: Natural Solutions (Thomas)
"""

import re
from datetime import datetime

from pyramid.view import view_config
from sqlalchemy import select, and_, insert, bindparam

from ecorelevesensor.models import DBSession, Rfid

prefix='rfid/'

@view_config(route_name=prefix+'import', renderer='string')
def rfid_import(request):
   data = []
   message = ""
   field_label = []
   isHead = False
   try:
      content = request.POST['data']
      if re.compile('\r\n').search(content):
         data = content.split('\r\n')
      elif re.compile('\n').search(content):
         data = content.split('\n')
      elif re.compile('\r').search(content):
         data = content.split('\r')

      fieldtype1 = {'NB':'no','TYPE':'type','"PUCE "':'code','DATE':'no','TIME':'no'}
      fieldtype2 = {'#':'no','Transponder Type:':'type','Transponder Code:':'code','Date:':'no','Time:':'no','Event:':'Event','Unit #:':'Unit','Antenna #:':'Antenna','Memo:':'Memo','Custom:':'Custom','':''}
      fieldtype3 = {'Transponder Type:':'type','Transponder Code:':'code','Date:':'no','Time:':'no','Event:':'Event','Unit #:':'Unit','Antenna #:':'Antenna','Memo:':'Memo','Custom:':'Custom'}

      entete = data[0]
      if re.compile('\t').search(entete):
         separateur = '\t'
      elif re.compile(';').search(entete):
         separateur = ';'
      entete = entete.split(separateur)
      #file with head
      if (sorted(entete) == sorted(fieldtype1.keys())):
         field_label = ["no","Type","Code","date","time"]
         isHead = True
      elif (sorted(entete) == sorted(fieldtype2.keys())):
         field_label = ["no","Type","Code","date","time","no","no","no","no","no"]
         isHead = True
      elif (sorted(entete) == sorted(fieldtype3.keys())):
         field_label = ["Type","Code","date","time","no","no","no","no","no"]
         isHead = True
      else:# without head
         isHead = False
         if separateur == ';':
            field_label = ["no","Type","Code","date","time","no","no","no","no","no"]
         else:
            if len(entete) > 5:
               field_label = ["Type","Code","date","time","no","no","no","no","no"]
               if entete[0] == 'Transponder Type:':
                  isHead = True
            else:
               field_label = ["no","Type","Code","date","time"]

      j=0
      code = ""
      date = ""
      dt = ""
      Rfids = []
      if (isHead):
         j=1
      #parsing data
      while j < len(data):
         i = 0
         if data[j] != "":
            row = data[j].replace('"','').split(separateur)
            while i < len(field_label):
               if field_label[i] == 'Code':
                  code = row[i]
               if field_label[i] == 'date':
                  date = row[i]
               if field_label[i] == 'time':
                  time = re.sub('\s','',row[i])
                  format_dt = '%d/%m/%Y %H:%M:%S'
                  if re.search('PM|AM',time):
                     format_dt = '%d/%m/%Y %I:%M:%S%p'
                  dt = date+' '+time
                  dt = datetime.strptime(dt, format_dt).strftime('%d-%m-%Y %H:%M:%S')
               i=i+1

         id_rfid = DBSession.execute(select([Rfid.pk_id]).where(and_(Rfid.chip_code == code,  Rfid.date == dt))).scalar()
         if id_rfid is None:
            Rfids.append({'chip_code':code, 'date_':dt})
         j=j+1

      if len(Rfids) > 0:
         if DBSession.execute(insert(Rfid), Rfids):
            message = str(len(Rfids))+' rows inserted'
      else:
         message = 'The data already exists'
   except Exception as e:
      message = e
   return message