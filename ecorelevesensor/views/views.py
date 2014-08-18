from collections import OrderedDict
from pyramid.view import view_config

from sqlalchemy import (
    Float,
    between,
    func,
    cast,
    Date,
    select,
    join, 
    and_,
    insert,
    bindparam
    )

import datetime, operator
import re, csv

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer   
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus.flowables import PageBreak 
from reportlab.lib import colors  

from ..models import DBSession, _Base
from ecorelevesensor.models.data import (
   Station,
   ViewRfid,
   MonitoredStation,
   ProtocolStationEquipment,
   ThemeEtude,
   MapSelectionManager,
   User,
   Protocole,
   )
from ..models.sensor import Argos, Gps, Rfid
from ..utils.spreadsheettable import SpreadsheetTable 

# Data imported from the CLS WS during the last week.
@view_config(route_name='weekData', renderer='json')
def weekData(request):
    """Return an array of location number per day within the last seven days."""
    today = datetime.date.today()
    # Initialize Json object
    data = {
        'label':[str(today - datetime.timedelta(days = i)) for i in range(1,8)],
        'nbArgos': [0] * 7,
        'nbGPS': [0] * 7
    }

    # Argos data
    argos_query = select(
        [cast(Argos.date, Date).label('date'), func.count(Argos.id).label('nb')]
        ).where(Argos.date >= today - datetime.timedelta(days = 7)
        ).group_by(cast(Argos.date, Date)
    )
    for date, nb in DBSession.execute(argos_query).fetchall():
        try:
            i = data['label'].index(str(date))
            data['nbArgos'][i] = nb
        except: pass

    # GPS data
    gps_query = select(
        [cast(Gps.date, Date).label('date'), func.count(Gps.id).label('nb')]
        ).where(Gps.date >= today - datetime.timedelta(days = 7)
        ).group_by(cast(Gps.date, Date))
    for date, nb in DBSession.execute(gps_query).fetchall():
        try:
            i = data['label'].index(str(date))
            data['nbGPS'][i] = nb
        except: pass
   
    return data

@view_config(route_name = 'station_graph', renderer = 'json')
def station_graph(request):
    # Initialize Json object
    result = OrderedDict()

    # Calculate the bounds
    today = datetime.date.today()
    begin_date = datetime.date(day=1, month=today.month, year=today.year-1)
    end_date = datetime.date(day=1, month=today.month, year=today.year)

    # Query
    query = select([
        func.count(Station.id).label('nb'),
        func.year(Station.date).label('year'),
        func.month(Station.date).label('month')]
        ).where(and_(Station.date >= begin_date, Station.date < end_date)
        ).group_by(func.year(Station.date), func.month(Station.date)
    )

    """ 
        Execute query and sort result by year, month
        (faster than an order_by clause in this case)
    """
    data = DBSession.execute(query).fetchall()
    for nb, y, m in sorted(data, key=operator.itemgetter(1,2)):
        d = datetime.date(day=1, month=m, year=y).strftime('%b')
        result[' '.join([d, str(y)])] = nb

    return result

@view_config(route_name = 'rfid_import', renderer = 'string')
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
                  dt = datetime.datetime.strptime(dt, format_dt).strftime('%d-%m-%Y %H:%M:%S')
               i=i+1
         
         id_rfid = DBSession.execute(select([Rfid.id]).where(and_(Rfid.code == code,  Rfid.date == dt))).scalar()
         if id_rfid is None:
            Rfids.append({'_code':code, '_date':dt})
         j=j+1 
      
      if len(Rfids) > 0:
         if DBSession.execute(insert(Rfid).values(code=bindparam('_code'), date=bindparam('_date')),Rfids):
            message = str(len(Rfids))+' rows inserted'
      else:
         message = 'The data already exists'
   except Exception as e:
      message = e   
   return message
   
@view_config(route_name = 'rfid_list', renderer = 'json')
def rfid_list(request):
   data = []
   try:
      for id in DBSession.execute(select([ViewRfid.id])).fetchall():
         data.append({'id':id[0]})
      return data
   except Exception as e:
      print(e)

@view_config(route_name = 'monitored_station_list', renderer = 'json')
def monitored_station_list(request):
   data = []
   try:
      for id in DBSession.execute(select([MonitoredStation.id])).fetchall():
         data.append({'id':id[0]})
      return data
   except Exception as e:
      print(e)

@view_config(route_name = 'rifd_monitored_add', renderer = 'string')
def rifd_monitored_add(request):
   message = ""
   try:
      begin_date = datetime.datetime.today().strftime('%d-%m-%Y %H:%M:%S')
      fk_rfid = request.GET['rfid']
      fk_geo = request.GET['site']
      if DBSession.execute(insert(ProtocolStationEquipment).values({"FK_RFID_obj":int(fk_rfid), "FK_GeoID":int(fk_geo), "beginDATE":begin_date})):
         message = 'Row inserted successfully '
   except Exception as e:
      message = e
   return message

@view_config(route_name = 'theme/list', renderer = 'json')
def theme_list(request):
   data = []
   try:
      j = join(ThemeEtude, MapSelectionManager, ThemeEtude.id == MapSelectionManager.TSMan_FK_Theme)
      query = select([ThemeEtude.id, ThemeEtude.Caption]).where(ThemeEtude.Actif == 1).group_by(ThemeEtude.id, ThemeEtude.Caption).order_by(ThemeEtude.Caption)
      try:
         if(request.GET['export'] is not None):
            query = query.select_from(j)
      except:
         pass
      for id, caption in DBSession.execute(query).fetchall():
         data.append({'id':id, 'caption': caption})
      try:
         if(request.GET['export'] is not None):
            data.append({'id':'null', 'caption': 'Others'})
      except:
         pass
   except Exception as e:
      print(e)
   return data

@view_config(route_name = 'core/user/fieldworkers', renderer = 'json')
def fieldWorkers(request):
    query = select([
        User.id, 
        User.fullname
    ]).order_by(User.lastname, User.firstname)
    data = DBSession.execute(query).fetchall()
    return [{'ID': user_id, 'Nom': fullname} for user_id, fullname in data]

@view_config(route_name = 'core/protocoles/list', renderer = 'string')
def protocoles_list(request):
   xml = "<protocoles>"
   try:
      for id, relation, caption, description in DBSession.execute(select([Protocole.id, Protocole.Relation, Protocole.Caption, Protocole.Description]).where(Protocole.Active == 1).order_by(Protocole.Caption)).fetchall():
         xml = xml + "<protocole id='"+str(id)+"'>"+caption+"</protocole>"
      xml = xml + "</protocoles>"
   except Exception as e:
      print(e)
   request.response.content_type = "text/xml"
   return xml

@view_config(route_name = 'core/views/list', renderer = 'string')
def views_list(request):
   xml = "<views>"
   try:
      query = select([MapSelectionManager.id, MapSelectionManager.TSMan_sp_name, MapSelectionManager.TSMan_Layer_Name, MapSelectionManager.TSMan_Description, MapSelectionManager.TSMan_FK_Theme]).order_by(MapSelectionManager.TSMan_Layer_Name)
      try:
         if request.GET['id_theme'] is not None:
            query = query.where(MapSelectionManager.TSMan_FK_Theme == request.GET['id_theme'])
      except Exception as e:
         print(e)
      for id, sp_name, layer_name, description, fk_theme in DBSession.execute(query).fetchall():
         xml = xml + "<view id='"+sp_name+"'>"+layer_name.replace("_", " ")+"</view>"
      xml = xml + "</views>"
   except Exception as e:
      print(e)
   request.response.content_type = "text/xml"
   return xml

@view_config(route_name = 'core/views/export/details', renderer = 'json')
def views_details(request):
   data = []
   try:
      name_vue = request.matchdict['name']
      table = _Base.metadata.tables['ecoReleve_Data.dbo.'+name_vue]
      print(table)
      for column in table.c:
         name_c = str(column.name)
         type_c = str(column.type)
         if re.compile('VARCHAR').search(type_c):
            type_c = 'string'
         data.append({'name':name_c, 'type':type_c})
      return data
   except Exception as e:
      print(e)

@view_config(route_name = 'core/views/export/count', renderer = 'json')
def views_count(request):
   try:
      name_vue = request.matchdict['name']
      table = _Base.metadata.tables['ecoReleve_Data.dbo.'+name_vue]
      count = DBSession.execute(table.count()).scalar()
      return count
   except Exception as e:
      print(e)

@view_config(route_name = 'core/views/export/filter/count', renderer = 'json')
def views_filter_count(request):
   try:
      name_vue = request.matchdict['name']
      table = _Base.metadata.tables['ecoReleve_Data.dbo.'+name_vue]
      criteria = request.params
      query = select([func.count(table.c.values()[0])])
      query = query_criteria(query, table, criteria)

      count = DBSession.execute(query).scalar()
      return count
   except Exception as e:
      print(e)

@view_config(route_name = 'core/views/export/filter/geo', renderer = 'json')
def views_filter(request):
   try:
      name_vue = request.matchdict['name']
      table = _Base.metadata.tables['ecoReleve_Data.dbo.'+name_vue]
      criteria = request.params
      result = {'type':'FeatureCollection', 'features':[]}
      query = select([cast(table.c['LAT'].label('lat'), Float), cast(table.c['LON'].label('lon'), Float), func.count(table.c.values()[0])]).group_by(table.c['LAT'].label('lat'), table.c['LON'])
      query = query_criteria(query, table, criteria)
      for lat, lon, nb in  DBSession.execute(query).fetchall():
         result['features'].append({'type':'Feature', 'properties':{'count': nb}, 'geometry':{'type':'Point', 'coordinates':[lon,lat]}})
      return result
   except Exception as e:
      print(e)

@view_config(route_name = 'core/views/export/filter/result', renderer = 'json')
def views_filter_result(request):
   try:
      name_vue = request.matchdict['name']
      table = _Base.metadata.tables['ecoReleve_Data.dbo.'+name_vue]
      criteria = request.params
      skip = 0
      limit = 10
      try:
         if criteria['skip']:
            skip = int(criteria['skip'])
      except:
         pass
      try:
         if criteria['limit']:
            limit = int(criteria['limit'])
      except:
         pass
      columns = []
      cols = []
      if criteria['columns']:
         columns.append(func.row_number().over(order_by=table.c.values()[0].asc()).label('Id'))
         cols = criteria['columns'].split(',')
         for col in cols:
            columns.append(table.c[col])
     
      #count
      query_count = select([func.count(table.c.values()[0])])
      query_count = query_criteria(query_count, table, criteria)
      count = DBSession.execute(query_count).scalar()
      # select data
      query = select(columns)
      query = query_criteria(query, table, criteria)
      query = query.order_by(table.c.values()[0].asc()).limit(limit).offset(skip)

      data = DBSession.execute(query).fetchall()
      result = {'count':str(count), 'values':[]}
      result['values'] = [dict(row) for row in data]
      for obj in result['values']:
         for key, item in obj.items():
               obj[key] = item
      return result
   except Exception as e:
      print(e)

@view_config(route_name = 'core/views/export/filter/export', renderer = 'json')
def views_filter_export(request):
   try:
      name_vue = request.matchdict['name']
      table = _Base.metadata.tables['ecoReleve_Data.dbo.'+name_vue]
      criteria = request.params
      today = datetime.datetime.today().strftime('%d_%m_%Y %H_%M_%S')
      name_file = name_vue+"_"+today
      columns = []
      cols = []
      if criteria['columns']:
            cols = criteria['columns'].split(',')
            for col in cols:
               columns.append(table.c[col])
      query = select(columns)
      query = query_criteria(query, table, criteria)
      rows = DBSession.execute(query).fetchall()

      # generated CSV file
      csv_file = csv.writer(open("Files/csv/"+name_file+".csv", "wb"))
      csv_file.writerow(cols)

      data = []
      for obj in rows:
         row = []
         row_csv = []
         for item in obj:
            row.append(item)
            try:
               row_csv.append(item.encode("utf-8"))
            except:
               row_csv.append(item)

         csv_file.writerow(row_csv)
         data.append(row)

      #generated GPX file
      gpx='<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n<gpx xmlns="http://www.topografix.com/GPX/1/1" creator="byHand" version="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\n'
      gpx_data = [dict(row) for row in rows]
      for obj in gpx_data:
         lat, lon, date, sitename = "", "", "", ""
         for key, item in obj.items():
            if key == "LAT":
               lat = str(item)
            elif key == "LON":
               lon = str(item)
            elif key == "DATE":
               date = str(item)
            elif key == "Site_name":
               sitename = str(item)
         gpx = gpx + "\n<wpt lat='"+lat+"' lon='"+lon+"'>\n<ele></ele>\n<time>"+date+"</time>\n<desc></desc>\n<name>"+sitename+"</name>\n<sym>Flag, Blue</sym>\n</wpt>\n";
      gpx = gpx + "</gpx>"
  
      file_gpx = open("Files/gpx/"+name_file+".gpx", "w")
      file_gpx.write(gpx)
      file_gpx.close()

      # generated PDF file
      table_font_size = 9
      if name_vue == "V_Qry_VIndiv_MonitoredLostPostReleaseIndividuals_LastStations":
         table_font_size = 8
         for key in range(len(cols)):
            if cols[key] == 'DATE':
               cols[key] = 'Date lastpos'
            elif cols[key] == 'Name_signal_type':
               cols[key] = 'Signal'
            elif cols[key] == 'MonitoringStatus@Station':
               cols[key] = 'Monitoring st.'
            elif cols[key] == 'SurveyType@Station':
               cols[key] = 'Servey type'
         cols.append('Date')
      else:
         cols.append('Date de saisie')
      
      cols.append('Vu')
      cols.append('Entendu')
      cols.append('Perdu')
      cols.append('Mort')
      cols.append('Repro')
      cols.append('No check')

      data.insert(0,cols)

      def addPageNumber(canvas, doc):
         page_num = canvas.getPageNumber()
         text = "Page %s" % page_num
         canvas.setFont('Times-BoldItalic', 9)
         canvas.drawRightString(145*mm, 5*mm, text)

      styleSheet = getSampleStyleSheet()
      doc = SimpleDocTemplate("Files/pdf/"+name_file+".pdf",pagesize=landscape(A4),rightMargin=72,leftMargin=72,topMargin=20,bottomMargin=18)
      Story=[]
       
      styles=getSampleStyleSheet()
      styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

      Story.append(Paragraph("Export "+name_vue, styleSheet['Title']))
      Story.append(Spacer(0, 5 * mm))
      if name_vue == "V_Qry_VIndiv_MonitoredLostPostReleaseIndividuals_LastStations":
         Story.append(Paragraph("Nom de l\'observateur:_____________________________",styleSheet['BodyText']))  
         Story.append(Paragraph("Secteur de suivi: _____________________ Date de Saisie: _________________",styleSheet['BodyText']))  
         Story.append(Spacer(0, 10 * mm))

      table_style = [  
        ('GRID', (0,0), (-1,-1), 1, colors.black),  
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),  
        ('LEFTPADDING', (0,0), (-1,-1), 3),  
        ('RIGHTPADDING', (0,0), (-1,-1), 3),  
        ('FONTSIZE', (0,0), (-1,-1), table_font_size),  
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),  
      ]  
      spreadsheet_table = SpreadsheetTable(data, repeatRows = 1)  
      spreadsheet_table.setStyle(table_style)  
      Story.append(spreadsheet_table)  
      Story.append(PageBreak()) 
      doc.build(Story, onFirstPage=addPageNumber, onLaterPages=addPageNumber)

      return name_file
   except: raise

def query_criteria(query, table, criteria):
   for column, value in criteria.items():
         if column in table.c:
            if re.search(',',value):
               sp = value.split(',')
               if sp[0] == 'IN':
                  if re.search('|',sp[1]):
                     data = sp[1].split('|')
                  else:
                     data = sp[1]
                  query = query.where(table.c[column].in_(data))
               elif sp[0] == 'LIKE':  
                  query = query.where(table.c[column].like('%'+sp[1]+'%'))
               elif sp[0] == '<':
                  query = query.where(table.c[column] < sp[1])
               elif sp[0] == '>':
                  query = query.where(table.c[column] > sp[1])
               elif sp[0] == '<>':
                  query = query.where(table.c[column] != sp[1])
               elif sp[0] == '=':
                  query = query.where(table.c[column] == sp[1])
            else:
               if value == 'IS NULL':
                  query = query.where(table.c[column].is_(None))
               elif value == 'IS NOT NULL':
                  query = query.where(table.c[column].isnot(None))
         else:
            if column == 'bbox':
               sp = value.split(',')
               query = query.where(and_(between(table.c['LAT'], float(sp[1]), float(sp[3])), between(table.c['LON'], float(sp[0]), float(sp[2]))))
   return query













