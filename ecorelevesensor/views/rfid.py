"""
Created on Thu Aug 28 16:45:25 2014
@author: Natural Solutions (Thomas)
"""

import re, operator, transaction


from datetime import datetime

from ecorelevesensor.utils.generator import Generator

from pyramid.view import view_config
from sqlalchemy import select, insert, text, desc, bindparam, or_, outerjoin, func, and_
from sqlalchemy.exc import IntegrityError
import json
from ecorelevesensor.models import (
    DBSession,
    DataRfid,
    dbConfig,
    Individual,
    MonitoredSite, 
    MonitoredSiteEquipment,
    MonitoredSitePosition,
    Base
)
from ecorelevesensor.models.object import ObjectRfid
from collections import OrderedDict

prefix='rfid/'

gene= Generator('RFID_MonitoredSite')

def get_operator_fn(op):
    return {
        '<' : operator.lt,
        '>' : operator.gt,
        '=' : operator.eq,
        '<>': operator.ne,
        '<=': operator.le,
        '>=': operator.ge,
        'Like': operator.eq,
        'Not Like': operator.ne,
        }[op]
def eval_binary_expr(op1, operator, op2):
    op1,op2 = op1, op2
    return get_operator_fn(operator)(op1, op2)

@view_config(route_name='rfid', renderer='json', request_method='GET')
def rfid_get(request):
    return DBSession.query(ObjectRfid).all()
    
@view_config(route_name='rfid', renderer='string', request_method='POST')
def rfid_add(request):
    try:
        obj = ObjectRfid()
        obj.identifier = request.json_body.get('identifier', None)
        obj.creator = request.authenticated_userid
        DBSession.add(obj)
        rfid = DBSession.query(ObjectRfid.id
            ).filter(ObjectRfid.identifier==obj.identifier).scalar()
        transaction.commit()
    except IntegrityError:
        request.response.status_code = 500
        return 'Error: An object with the same identifier already exists.'
    return ' '.join(['Success: RFID module created with ID =', str(rfid), '.'])

@view_config(route_name=prefix+'byName', renderer='json')
def rfid_detail(request):
    name = request.matchdict['name']
    data = DBSession.query(ObjectRfid, MonitoredSite, MonitoredSiteEquipment
        ).outerjoin(MonitoredSiteEquipment, ObjectRfid.id==MonitoredSiteEquipment.obj
        ).outerjoin(MonitoredSite, MonitoredSiteEquipment.site==MonitoredSite.id
        ).filter(ObjectRfid.identifier==name
        ).order_by(desc(MonitoredSiteEquipment.begin_date)).first()
    module, site, equip = data
    result = {'module': module, 'site':site, 'equip':equip}
    return result

@view_config(route_name=prefix+'byDate', renderer='json')
def rfid_active_byDate(request):
    date = datetime.strptime(request.params['date'], '%d/%m/%Y  %H:%M:%S')
    data = DBSession.query(MonitoredSite.id, MonitoredSite.name, MonitoredSite.type_,  MonitoredSitePosition.lat,  MonitoredSitePosition.lon
        ).join(MonitoredSitePosition, MonitoredSite.id==MonitoredSitePosition.id
        ).filter(MonitoredSitePosition.end_date == None ).all()
    siteName_type=[{'id_site':row[0] ,'type':row[2] , 'name':row[1], 'positions': {'lat': row[3], 'lon': row[4] }} for row in data]
    result = {'siteType': list(set([row[2] for row in data])), 'siteName_type': siteName_type}
    return result

@view_config(route_name=prefix+'identifier', renderer='json')
def rfid_get_identifier(request):
    query = select([ObjectRfid.identifier]).where(ObjectRfid.type_=='rfid')
    data =  DBSession.execute(query).fetchall()
    transaction.commit()
    return [row[0] for row in data]

@view_config(route_name=prefix+'import', renderer='string')
def rfid_import(request):
    data = []
    message = ""
    field_label = []
    isHead = False
    now=datetime.now()
    try:
        creator = request.authenticated_userid
        content = request.POST['data']
        module = request.POST['module']
        idModule = DBSession.execute(select([ObjectRfid.id]).where(ObjectRfid.identifier==module)).scalar();
     
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
                elif entete[1] == 'Transponder Type:':
                    isHead = True
                    field_label = ["no","Type","Code","date","time"]
                else:
                    field_label = ["no","Type","Code","date","time"]

        j=0
        code = ""
        date = ""
        dt = ""
        Rfids, chip_codes = set(), set()
        if (isHead):
            j=1
        #parsing data
        allDate = []
        while j < len(data):
            i = 0
            if data[j] != "" :
                line = data[j].replace('"','').split(separateur)
                while i < len(field_label):
                    if field_label[i] == 'Code':
                        code = line[i]
                    if field_label[i] == 'date':
                        date = line[i]
                    if field_label[i] == 'time':
                        time = re.sub('\s','',line[i])
                        format_dt = '%d/%m/%Y %H:%M:%S'
                        if re.search('PM|AM',time):

                            format_dt = '%m/%d/%Y %I:%M:%S%p'
                            format_dtBis='%d/%m/%Y %I:%M:%S%p'
                        dt = date+' '+time
                        try :
                            dt = datetime.strptime(dt, format_dt)
                        except Exception as e:

                            dt = datetime.strptime(dt, format_dtBis)
                        allDate.append(dt)

                    i=i+1
                Rfids.add((creator, idModule, code, dt))
                chip_codes.add(code)
            j=j+1

        ## check if Date corresponds with pose remove module ##
        table = Base.metadata.tables['RFID_MonitoredSite']
        q_check_date = select([func.count('*')]).where(
            and_(table.c['begin_date'] < allDate[0], or_(table.c['end_date'] >= allDate[-1],table.c['end_date'] == None))
            ).where(table.c['identifier'] == module)
        check = DBSession.execute(q_check_date).scalar() 
        if check == 0 :
            request.response.status_code = 510
            message = "Dates of this uploded file (first date : "+str(allDate[0])+" , last date : "+str(allDate[-1])+") don't correspond with the deploy/remove dates of the selected module"
            return message

        Rfids = [{DataRfid.creator.name: crea, DataRfid.obj.name: idMod, DataRfid.checked.name: '0',
                DataRfid.chip_code.name: c, DataRfid.date.name: d, DataRfid.creation_date.name: now} for crea, idMod, c, d  in Rfids]
        # Insert data.
        DBSession.execute(insert(DataRfid), Rfids)
        message = str(len(Rfids)) +' rows inserted.'
        # Check if there are unknown chip codes.
        query = select([Individual.chip_code]).where(Individual.chip_code.in_(chip_codes))
        known_chips = set([row[0] for row in DBSession.execute(query).fetchall()])
        unknown_chips = chip_codes.difference(known_chips)
        if len(unknown_chips) > 0:
            message += '\n\nWarning : chip codes ' + str(unknown_chips) + ' are unknown.'
    except IntegrityError as e:
        request.response.status_code = 500
        message = 'Data already exist.'
    except Exception as e:
        print(e)
        request.response.status_code = 520
        message = 'Error'
    return message

@view_config(route_name=prefix+'validate', renderer='string')
def rfid_validate(request):
    #TODO: SQL SERVER specific code removal
    checked = request.GET['checked']
    frequency_hour = request.GET['frequency_hour']
    stmt = text("""
        DECLARE @error int, @nb int, @exist int;
        EXEC """ + dbConfig['data_schema'] + """.sp_validate_rfid :checked, :frequency_hour, :user, @nb OUTPUT,@exist OUTPUT, @error OUTPUT;
        SELECT @error, @nb,@exist;"""
    ).bindparams(bindparam('user', request.authenticated_userid),bindparam('frequency_hour', frequency_hour),bindparam('checked', 0))
    error_code, nb, exist = DBSession.execute(stmt).fetchone()
    if nb > 0:
        return 'Success : ' + str(nb) + ' new rows inserted in table T_AnimalLocation, '+str(exist)+' existing'
    else:
        return 'Warning : no new row inserted.'

@view_config(route_name=prefix + 'validate/search', renderer='json', request_method='GET')
def rfids_search(request):

    data_helper= Generator('V_dataRFID_as_file')
    criteria=[{'Column':'checked','Operator':'=', 'Value': 0}]      
    if(request.GET.get('offset')):
        offset = json.loads(request.GET.get('offset',{}))
        perPage = json.loads(request.GET.get('per_page',{}))
        orderBy = json.loads(request.GET.get('order_by',{}))
        content = data_helper.get_search(criteria, offset=offset, per_page=perPage, order_by=orderBy)
    else :
        content = data_helper.get_search(criteria)
    
    return content

@view_config(route_name=prefix + 'validate/search', renderer='json', request_method='POST')
def rfids_update(request):

    data_helper= Generator('V_dataRFID_as_file')
    data=request.json_body
    gene.update_data(data,'PK_id')
    data_helper.update_data(data,'PK_obj')

@view_config(route_name=prefix + 'validate/getFields', renderer='json', request_method='GET')
def rfids_field(request):

    data_helper= Generator('V_dataRFID_as_file')
    colist=[
    {'name':'identifier','label':'Identifier','display':False,'edit':False},
    {'name':'checked','label':'CHECKED','display':False, 'edit':False},
    {'name':'nb_chip_code','label':'NB DIFFERENT CHIP CODE','display':True, 'edit':False},
    {'name':'total_scan','label':'TOTAL SCAN','display':True, 'edit':False},
    {'name':'creation_date','label':'CREATION DATE','display':True, 'edit':False},
    {'name':'frequency_hour','label':'FREQUENCY','display':False, 'edit':False},
    {'name':'first_scan','label':'First scan','display':True, 'edit':False},
    {'name':'last_scan','label':'Last scan','display':True, 'edit':False},
    {'name':'site_name','label':'Site Name','display':True, 'edit':False},
    {'name':'site_type','label':'Site Type','display':True, 'edit':False},
    ]
    check = request.GET.get('checked') == 'true'
    cols = data_helper.get_col(colist, checked=check)
    return cols

@view_config(route_name=prefix + 'validate/getFilters', renderer='json', request_method='GET')
def rfids_filters(request):

    table=Base.metadata.tables['RFID_MonitoredSite']
    columns=[table.c['identifier'],table.c['begin_date'],table.c['end_date'],table.c['Name'],table.c['name_Type']]  
    final={}
    for col in columns :
        name=col.name
        Ctype=str(col.type)
        if 'VARCHAR' in Ctype:
            Ctype='String'
        final[name]=Ctype
    return final

@view_config(route_name=prefix + 'search_geoJSON', renderer='json', request_method='POST')
def rfids_geoJSON(request):

    table=Base.metadata.tables['RFID_MonitoredSite']
    criteria = request.json_body.get('criteria', {})
    query = select(table.c)
    for obj in criteria:
        query=query.where(eval_binary_expr(table.c[obj['Column']], obj['Operator'], obj['Value']))
    data=DBSession.execute(query).fetchall()    
    geoJson=[]
    for row in data:
        geoJson.append({'type':'Feature', 'properties':{'name':row['Name']}, 'geometry':{'type':'Point', 'coordinates':[row['lon'],row['lat']]}})
    return {'type':'FeatureCollection', 'features':geoJson}

@view_config(route_name=prefix + 'update', renderer='json', request_method='POST')
def rfid_update(request):
    data = request.body
    rfid = json.loads(request.body.decode(encoding='UTF-8'))
    table=Base.metadata.tables['RFID_MonitoredSite']
    query = select(table.c)
  
@view_config(route_name=prefix + 'pose/getFields', renderer='json', request_method='GET')
def rfid_pose_filters(request):

    data_helper= Generator('RFID_MonitoredSite')
    colist=[
    {'name':'PK_obj','label':'ID_Obj','display':False,'edit':False},
    {'name':'identifier','label':'Identifier','display':True, 'edit':False},
    {'name':'begin_date','label':'Begin Date','display':True, 'edit':False},
    {'name':'end_date','label':'End Date','display':True, 'edit':False},
    {'name':'Name','label':'Site Name','display':True, 'edit':False},
    {'name':'name_Type','label':'Site Type','display':True, 'edit':False},
    ]
    check = request.GET.get('checked') == 'true'
    cols = data_helper.get_col(colist, checked=check)
    return cols

@view_config(route_name=prefix + 'pose/search', renderer='json', request_method='GET')
def rfids_update(request):

    data_helper= Generator('RFID_MonitoredSite')
    criteria=json.loads(request.params.get('criteria',{}))
    result = data_helper.get_search(criteria,offset=0,per_page=0, order_by={'begin_date:desc'})
    return result
