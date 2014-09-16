"""
Created on Thu Aug 28 16:45:25 2014

@author: Natural Solutions (Thomas)
"""

import re
from datetime import datetime

from pyramid.view import view_config
from sqlalchemy import select, insert, text, desc, bindparam
from sqlalchemy.exc import IntegrityError

from ecorelevesensor.models import (
    DBSession,
    DataRfid,
    dbConfig,
    Individual,
    MonitoredSite, 
    MonitoredSiteEquipment
)
from ecorelevesensor.models.object import ObjectRfid

prefix='rfid/'

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

@view_config(route_name=prefix+'identifier', renderer='json')
def rfid_get_identifier(request):
    query = select([ObjectRfid.identifier]).where(ObjectRfid.type_=='rfid')
    return [row[0] for row in DBSession.execute(query).fetchall()]

@view_config(route_name=prefix+'import', renderer='string')
def rfid_import(request):
    data = []
    message = ""
    field_label = []
    isHead = False
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
        while j < len(data):
            i = 0
            if data[j] != "":
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
                            format_dt = '%d/%m/%Y %I:%M:%S%p'
                        dt = date+' '+time
                        dt = datetime.strptime(dt, format_dt)
                    i=i+1
                Rfids.add((creator, idModule, code, dt))
                chip_codes.add(code)
            j=j+1
        Rfids = [{DataRfid.creator.name: crea, DataRfid.obj.name: idMod, 
                DataRfid.chip_code.name: c, DataRfid.date.name: d} for crea, idMod, c, d  in Rfids]
        # Insert data.
        DBSession.execute(insert(DataRfid), Rfids)
        message = str(len(Rfids)) +' rows inserted.'
        # Check if there are unknown chip codes.
        query = select([Individual.chip_code]).where(Individual.chip_code.in_(chip_codes))
        known_chips = set([row[0] for row in DBSession.execute(query).fetchall()])
        unknown_chips = chip_codes.difference(known_chips)
        if len(unknown_chips) > 0:
            message += '\n\nWarning : chip codes ' + str(unknown_chips) + ' are invalid.'
    except IntegrityError as e:
        request.response.status_code = 500
        message = 'Error : data already exist.\n\nDetail :\n' + str(e.orig)
    except Exception as e:
        request.response.status_code = 500
        message = e
    return message

@view_config(route_name=prefix+'validate', renderer='string')
def rfid_validate(request):
    #TODO: SQL SERVER specific code removal
    stmt = text("""
        DECLARE @error int, @nb int;
        EXEC """ + dbConfig['data_schema'] + """.sp_validate_rfid :user, @nb OUTPUT, @error OUTPUT;
        SELECT @error, @nb;"""
    ).bindparams(bindparam('user', request.authenticated_userid))
    error_code, nb = DBSession.execute(stmt).fetchone()
    if error_code == 0:
        if nb > 0:
            return 'Success : ' + str(nb) + ' new rows inserted in table T_AnimalLocation.'
        else:
            return 'Warning : no new row inserted.'
    else:
        return 'Error : an error occured during validation process (error code : ' + str(error_code) + ' )'

