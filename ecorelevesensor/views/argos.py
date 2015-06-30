from array import array

from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy import func, desc, select, union, union_all, and_, bindparam, update, or_, literal_column, join, text
import json
from pyramid.httpexceptions import HTTPBadRequest
from ecorelevesensor.utils.data_toXML import data_to_XML
import pandas as pd
import numpy as np
import transaction, time
from ecorelevesensor.models import DBSession
from ecorelevesensor.models.sensor import Argos, Gps, ArgosGps,ArgosEngineering
from ecorelevesensor.models import Individual, dbConfig
from ecorelevesensor.models.data import (
    V_dataARGOS_withIndivEquip,
    V_dataGPS_withIndivEquip,
    V_dataARGOS_GPS_with_IndivEquip,
    ProtocolArgos,
    ProtocolGps,
    ProtocolIndividualEquipment,
    SatTrx,
    Station,
    V_Individuals_LatLonDate
)
from ecorelevesensor.utils.distance import haversine
import win32con, win32gui, win32ui, win32service, os, time, re
from win32 import win32api
import shutil
from time import sleep
import subprocess 
from pyramid.security import NO_PERMISSION_REQUIRED
import ecorelevesensor
from datetime import datetime

route_prefix = 'argos/'
def asInt(s):
    try:
        return int(s)
    except:
        return None
# List all PTTs having unchecked locations, with individual id and number of locations.
@view_config(
        route_name='{type}/unchecked/list',
        # permission='read',
        renderer='json')
def argos_unchecked_list(request):
        """Returns the unchecked Argos data summary.
        """
        type_= request.matchdict['type']
        if type_ == 'argos' :
            unchecked = V_dataARGOS_GPS_with_IndivEquip
        elif type_ == 'gsm' :
            unchecked = V_dataGSM_withIndivEquip

        unchecked_with_ind = select([unchecked.ptt.label('platform_'),
            unchecked.ind_id, unchecked.begin_date, unchecked.end_date,
            func.count().label('nb'), func.max(unchecked.date_).label('max_date'),
            func.min(unchecked.date_).label('min_date')]).where(unchecked.checked == 0
            ).group_by(unchecked.ptt, unchecked.ind_id, unchecked.begin_date, unchecked.end_date
            ).order_by(unchecked.ind_id.desc())
        # Populate Json array
        data = DBSession.execute(unchecked_with_ind).fetchall()
        return [dict(row) for row in data]


@view_config(route_name=route_prefix + 'unchecked/count', renderer='json')
def argos_unchecked_count(request):
        """Returns the unchecked argos data count."""
        return DBSession.query(func.count(Argos.pk)
                ).filter(Argos.checked == False).scalar()
     
@view_config(route_name = 'gps/unchecked/count', renderer = 'json')
def gps_unchecked_count(request):
        """Returns the unchecked gps data count."""
        return {'count': DBSession.query(func.count(Gps.pk)
                ).filter(Gps.checked == 0).scalar()}

@view_config(route_name = 'argos/import', renderer = 'json')
def argos_manual_validate(request) :

    ptt = request.matchdict['id']
    data = request.json_body.get('data')
    ind_id = request.matchdict['ind_id']
    type_ = request.matchdict['type']
    ind_id = asInt(ind_id)
    
    try : 
        if isinstance( ind_id, int ): 
            xml_to_insert = data_to_XML(data)
            # validate unchecked ARGOS_ARGOS or ARGOS_GPS data from xml data PK_id.         
            start = time.time()
            # push xml data to insert into stored procedure in order ==> create stations and protocols if not exist
            stmt = text(""" DECLARE @nb_insert int , @exist int, @error int;

                exec """+ dbConfig['data_schema'] + """.[sp_validate_argosArgos_argosGPS] :id_list, :ind_id , :user , :ptt , @nb_insert OUTPUT, @exist OUTPUT , @error OUTPUT;
                    SELECT @nb_insert, @exist, @error; """
                ).bindparams(bindparam('id_list', xml_to_insert),bindparam('ind_id', ind_id),bindparam('user', request.authenticated_userid),bindparam('ptt', ptt))
            nb_insert, exist , error = DBSession.execute(stmt).fetchone()
            transaction.commit()

            stop = time.time()
            return str(nb_insert)+' stations/protocols was inserted, '+str(exist)+' are already existing and '+str(error)+' error(s)'
        else : 
            return error_response(None)
    except  Exception as err :
        return error_response(err)

@view_config(route_name=route_prefix + 'import/auto', renderer='json', request_method='POST')
def data_argos_validation_auto(request):
    try :
        ptt = request.matchdict['id']
        ind_id = request.matchdict['ind_id']
        type_ = request.matchdict['type']
        print (ind_id)
        if ind_id != None: 
            ind_id = asInt(ind_id)
            nb_insert, exist , error = auto_validate_argos_gps(ptt,ind_id,request.authenticated_userid,type_)
            return str(nb_insert)+' stations/protocols was inserted, '+str(exist)+' are already existing and '+str(error)+' error(s)'
        else : 
            return error_response(None)
    except  Exception as err :
        return error_response(err)

def error_response (err) : 
        
        if err !=None : 
            msg = err.args[0] if err.args else ""
            response=Response('Problem occurs : '+str(type(err))+' = '+msg)
        else : 
            response=Response('No induvidual is equiped with this ptt at this date')
        response.status_int = 500
        return response

@view_config(route_name=route_prefix + 'importAll/auto', renderer='json', request_method='POST')
def data_argos_ALL_validation_auto(request):
    unchecked_list = argos_unchecked_list(request)
    type_ = request.matchdict['type']
    Total_nb_insert = 0
    Total_exist = 0
    Total_error = 0
    start = time.time()
    try : 
        for row in unchecked_list : 
            ptt = row['platform_']
            ind_id = row['ind_id']

            if ind_id != None : 
                nb_insert, exist, error = auto_validate_argos_gps(ptt,ind_id,request.authenticated_userid, type_)
                Total_exist += exist
                Total_nb_insert += nb_insert
                Total_error += error
        stop = time.time()
        return str(Total_nb_insert)+' stations/protocols was inserted, '+str(Total_exist)+' are already existingand '+str(Total_error)+' error(s)'
    except  Exception as err :

        msg = err.args[0] if err.args else ""
        response=Response('Problem occurs  : '+str(type(err))+' = '+msg)
        response.status_int = 500
        return response

def auto_validate_argos_gps (ptt,ind_id,user,type_) :
    start = time.time()
    stmt = text(""" DECLARE @nb_insert int , @exist int , @error int;

        exec """+ dbConfig['data_schema'] + """.[sp_auto_validate_argosArgos_argosGPS] :ptt , :ind_id , :user , @nb_insert OUTPUT, @exist OUTPUT, @error OUTPUT;
            SELECT @nb_insert, @exist, @error; """
        ).bindparams(bindparam('ptt', ptt), bindparam('ind_id', ind_id),bindparam('user', user))
    nb_insert, exist , error= DBSession.execute(stmt).fetchone()
    transaction.commit()

    stop = time.time()
    return nb_insert, exist , error

@view_config(route_name = 'argos/check', renderer = 'json')
def argos_check(request):
     argos_id = array('i')
     gps_id = array('i')
     try:
            for ptt_obj in request.json_body:
                 ptt = ptt_obj['ptt']
                 ind_id = ptt_obj['ind_id']
                 for location in ptt_obj['locations']:
                        if location['type'] == 0:
                             argos_id.append(location['id'])
                        elif location['type'] == 1:
                             gps_id.append(location['id'])
            DBSession.execute(update(Argos).where(Argos.id.in_(argos_id)).values(checked=True))
            DBSession.execute(update(Gps).where(Gps.id.in_(gps_id)).values(checked=True))
            return {'argosChecked': len(argos_id), 'gpsChecked':len(gps_id)}
     except Exception as e:
            raise


@view_config(route_name= 'argos/details', renderer='json')
def indiv_details(request):
    type_= request.matchdict['type']
    unchecked = V_dataARGOS_GPS_with_IndivEquip
    ptt = int(request.matchdict['id'])
    ind_id = int(request.matchdict['ind_id'])
    join_table = join(Individual,unchecked, Individual.id == unchecked.ind_id) 

    query = select([Individual.id.label('ind_id'),
        Individual.survey_type.label('survey_type'),
        Individual.status.label('status'),
        Individual.monitoring_status.label('monitoring_status'),
        Individual.ptt.label('ptt'),
        Individual.species.label('species'),
        Individual.breeding_ring.label('breeding_ring'),
        Individual.release_ring.label('release_ring'),
        Individual.chip_code.label('chip_code'),
        Individual.sex.label('sex'),
        Individual.origin.label('origin'),
        Individual.age.label('age'),
        unchecked.begin_date,
        unchecked.end_date]).select_from(join_table).where(and_(unchecked.ptt == ptt,unchecked.ind_id == ind_id)
                                                              ).order_by(desc(unchecked.begin_date))
    data = DBSession.execute(query).first()
    transaction.commit()
    result = dict([ (key[0],key[1]) for key in data.items()])
    query = select([V_Individuals_LatLonDate.c.date]).where(V_Individuals_LatLonDate.c.ind_id == result['ind_id']).order_by(desc(V_Individuals_LatLonDate.c.date)).limit(1)  
    lastObs = DBSession.execute(query).fetchone()
    result['last_observation'] = lastObs['date'].strftime('%d/%m/%Y')
    result['ptt'] = ptt
    return result

# Unchecked data for one PTT.
@view_config(route_name='argos/unchecked/format', renderer='json')
def argos_unchecked_get_format (request):
    format_ = request.matchdict['format']
    platform = int(request.matchdict['id'])
    ind_id = request.matchdict['ind_id']

    if format_ == 'json' : 
        return argos_unchecked_json(platform,ind_id)
    elif format_ == 'geo' : 
        return argos_unchecked_geo(platform,ind_id)

def argos_unchecked_geo(platform,ind_id):
    """Returns list of unchecked locations for a given ptt."""
    unchecked = V_dataARGOS_GPS_with_IndivEquip

    if (ind_id != 'null') :
        ind_id = int(ind_id)
    else :
        ind_id = None

    query = select([unchecked.data_PK_ID.label('id'),
        unchecked.lat,
        unchecked.lon,
        unchecked.date_.label('date'),
        unchecked.ele,
        unchecked.type_]).where(and_(unchecked.ptt == platform,unchecked.ind_id == ind_id)).where(unchecked.checked == 0).order_by(desc(unchecked.date_))
    data = DBSession.execute(query).fetchall()
    features = [
        {
            'type':'Feature',
            'properties':{'date':str(date),'type':type_},
            'geometry':{'type':'Point', 'coordinates':[float(lon),float(lat)]},
            'id':id_
        }
    for id_, lat, lon, date, ele, type_ in data]
    transaction.commit()
    result = {'type':'FeatureCollection', 'features':features}
    return result

def argos_unchecked_json(platform,ind_id):  
        unchecked = V_dataARGOS_GPS_with_IndivEquip

        if (ind_id != 'null') :
            ind_id = int(ind_id)
        else :
            ind_id = None
        query = select([unchecked.data_PK_ID.label('id'),
        unchecked.lat,
        unchecked.lon,
        unchecked.date_.label('date'),
        unchecked.ele,
        unchecked.type_]).where(and_(unchecked.ptt == platform,unchecked.ind_id == ind_id)).where(unchecked.checked == 0).order_by(desc(unchecked.date_))

        data = DBSession.execute(query).fetchall()
        # Load data from the DB then
        # compute the distance between 2 consecutive points.
         
        df = pd.DataFrame.from_records(data, columns=data[0].keys(), coerce_float=True)
        X1 = df.iloc[:-1][['lat', 'lon']].values
        X2 = df.iloc[1:][['lat', 'lon']].values
        df['dist'] = np.append(haversine(X1, X2), 0).round(3)
        # Compute the speed
        df['speed'] = (df['dist'] / ((df['date'] - df['date'].shift(-1)).fillna(1) / np.timedelta64(1, 'h'))).round(3)
        # Values to import : the first per hour
        ids = df.set_index('date').resample('1H', how='first').dropna().id.values
        df['import'] = df.id.isin(ids)
        df['date'] = df['date'].apply(str) 
        # Fill NaN
        df.fillna(value={'ele':-999}, inplace=True)
        df.fillna(value={'speed':0}, inplace=True)
        df.replace(to_replace = {'speed': np.inf}, value = {'speed':9999}, inplace = True)
        return df.to_dict('records')

@view_config(route_name=route_prefix, renderer='json' ,request_method='POST',permission = NO_PERMISSION_REQUIRED)
def uploadFile(request) :
    import getpass
    username =  getpass.getuser()
    print ('*********************** UPLOAD ARGOS **************************')
    tmp_path = os.path.join(os.path.expanduser('~%s' % username), "AppData", "Local", "Temp")
    import_path = os.path.join(tmp_path, "ecoReleve_import")
    if not os.path.exists(import_path):
        os.makedirs(import_path)

    DS_path = os.path.join(tmp_path, "ecoReleve_import")

    if not os.path.exists(DS_path):
        os.makedirs(DS_path)

    file_obj = request.POST['file']
    filename = request.POST['file'].filename
    input_file = request.POST['file'].file

    full_filename = os.path.join(DS_path, filename)
    input_file.seek(0)
    with open(full_filename, 'wb') as output_file :
        shutil.copyfileobj(input_file, output_file)

    if 'DIAG' in filename :
        return parseDIAGFileAndInsert(full_filename)
    elif 'DS' in filename :
        return parseDSFileAndInsert(full_filename)

def parseDSFileAndInsert(full_filename):
    import getpass
    username =  getpass.getuser()
    workDir = os.path.dirname(os.path.dirname(os.path.abspath(ecorelevesensor.__file__)))
    con_file = os.path.join(workDir,'init.txt')
    MTI_path = os.path.join(workDir,'MTIwinGPS.exe')
    out_path = os.path.join(os.path.expanduser('~%s' % username), "AppData", "Local", "Temp",os.path.splitext(os.path.basename(full_filename))[0])
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    with open(con_file,'w') as f: 
        f.write("-eng\n")
        f.write("-argos\n")
        f.write("-title\n")
        f.write("-out\n")
        f.write(out_path+"\n")
        f.write(full_filename)

    args = [MTI_path]
    os.startfile(args[0])
    # p = subprocess.Popen([args[0]])
    hwnd = 0
    while hwnd == 0 :
        sleep(0.3)
        hwnd = win32gui.FindWindow(0, "MTI Argos-GPS Parser")

    btnHnd= win32gui.FindWindowEx(hwnd, 0 , "Button", "Run")

    win32api.SendMessage(btnHnd, win32con.BM_CLICK, 0, 0)
    
    

    filenames = [os.path.join(out_path,fn) for fn in next(os.walk(out_path))[2]]
    win32api.SendMessage(hwnd, win32con.WM_CLOSE, 0,0);

    for filename in filenames:
        fullname = os.path.splitext(os.path.basename(filename))[0]
        ptt = int(fullname[0:len(fullname)-1])

        if filename.endswith("g.txt"):
            tempG = pd.read_csv(filename,sep='\t',header=0 , parse_dates = [0], infer_datetime_format = True)
            tempG['ptt'] = ptt
            try:
                GPSData = GPSData.append(tempG)
            except :
                GPSData = tempG

        if filename.endswith("e.txt"):
            usecols= ['txDate','pttDate','satId','activity','txCount','temp','batt','fixTime','satCount','resetHours','fixDays','season','shunt','mortalityGT','seasonalGT']
            tempEng = pd.read_csv(filename,sep='\t',parse_dates=True,header = None, skiprows = [0])
            if len(tempEng.columns )== 17:

                usecols.append('latestLat')
                usecols.append('latestLon')
            tempEng.columns = usecols
            tempEng['ptt'] = ptt
            try:
                EngData = EngData.append(tempEng)
            except :
                EngData = tempEng

    EngToInsert = checkExistingEng(EngData)
    dataEng_to_insert = json.loads(EngToInsert.to_json(orient='records',date_format='iso'))
    if len(dataEng_to_insert) != 0 :
        stmt = ArgosEngineering.__table__.insert()#.values(dataGPS_to_insert[0:2])
        res = DBSession.execute(stmt,dataEng_to_insert)

    DFToInsert = checkExistingGPS(GPSData)
    dataGPS_to_insert = json.loads(DFToInsert.to_json(orient='records',date_format='iso'))

    if len(dataGPS_to_insert) != 0 :
        stmt = ArgosGps.__table__.insert()#.values(dataGPS_to_insert[0:2])
        res = DBSession.execute(stmt,dataGPS_to_insert)

    shutil.rmtree(out_path)

    return len(dataGPS_to_insert)

def checkExistingEng(EngData) :
    EngData['id'] = range(EngData.shape[0])
    maxDate = EngData['pttDate'].max(axis=1)
    minDate = EngData['pttDate'].min(axis=1)

    queryEng = select([ArgosEngineering.fk_ptt, ArgosEngineering.pttDate, ArgosEngineering.txDate])
    queryEng = queryEng.where(and_(ArgosEngineering.pttDate >= minDate , ArgosEngineering.pttDate <= maxDate))
    data = DBSession.execute(queryEng).fetchall()

    EngRecords = pd.DataFrame.from_records(data
        ,columns=[ArgosEngineering.fk_ptt.name, ArgosEngineering.pttDate.name, ArgosEngineering.txDate.name])

    merge = pd.merge(EngData,EngRecords, left_on = ['pttDate','txDate','ptt'], right_on = ['pttDate','txDate','FK_ptt'])
    DFToInsert = EngData[~EngData['id'].isin(merge['id'])]
    DFToInsert['FK_ptt'] = DFToInsert['ptt']
    DFToInsert = DFToInsert.drop(['id','ptt'],1)

    return DFToInsert

def checkExistingGPS (GPSData) :
    GPSData['datetime'] = GPSData.apply(lambda row: np.datetime64(row['Date/Time']).astype(datetime), axis=1)
    GPSData['id'] = range(GPSData.shape[0])
    maxDateGPS = GPSData['datetime'].max(axis=1)
    minDateGPS = GPSData['datetime'].min(axis=1)
    GPSData['Latitude(N)'] = np.round(GPSData['Latitude(N)'],decimals = 5)
    GPSData['Longitude(E)'] = np.round(GPSData['Longitude(E)'],decimals = 5)
    
    
    print ('\n\n********************* DATE **********************\n')
    # print(GPSData['datetime'][:0])
    queryGPS = select([ArgosGps.pk_id, ArgosGps.date, ArgosGps.lat, ArgosGps.lon, ArgosGps.ptt]).where(ArgosGps.type_ == 'gps')
    queryGPS = queryGPS.where(and_(ArgosGps.date >= minDateGPS , ArgosGps.date <= maxDateGPS))
    data = DBSession.execute(queryGPS).fetchall()

    GPSrecords = pd.DataFrame.from_records(data
        ,columns=[ArgosGps.pk_id.name, ArgosGps.date.name, ArgosGps.lat.name, ArgosGps.lon.name, ArgosGps.ptt.name]
        , coerce_float=True )


    GPSrecords['lat'] = GPSrecords['lat'].astype(float)
    GPSrecords['lon'] = GPSrecords['lon'].astype(float)

    merge = pd.merge(GPSData,GPSrecords, left_on = ['datetime','Latitude(N)','Longitude(E)','ptt'], right_on = ['date','lat','lon','FK_ptt'])
    DFToInsert = GPSData[~GPSData['id'].isin(merge['id'])]

    DFToInsert = DFToInsert.drop(['id','datetime'],1)
    DFToInsert.columns = ['date','lat','lon','speed','course','ele','FK_ptt']

    DFToInsert = DFToInsert.replace('2D fix',np.nan )
    DFToInsert = DFToInsert.replace('low alt',np.nan )
    DFToInsert['type']='gps'

    return DFToInsert

def parseDIAGFileAndInsert(full_filename):

    with open(full_filename,'r') as f:
        content = f.read()
        content = re.sub('\s+Prog+\s\d{5}',"",content)
        content2 = re.sub('[\n\r]\s{10,14}[0-9\s]+[\n\r]',"\n",content)
        content2 = re.sub('[\n\r]\s{10,14}[0-9\s]+$',"\n",content2)
        content2 = re.sub('^[\n\r\s]+',"",content2)
        content2 = re.sub('[\n\r\s]+$',"",content2)
        splitBlock = 'm[\n\r]'

        blockPosition = re.split(splitBlock,content2)

    colsInBlock = ['FK_ptt','date','lc','iq','lat1'
        ,'lon1','lat2','lon2','nbMsg','nbMsg120'
        ,'bestLevel','passDuration','nopc', 'freq','ele']
    ListOfdictParams = []
    j = 0
    for block in blockPosition :
        
        block = re.sub('[\n\r]+',"",block)
        block = re.sub('[a-zA-Z]\s+Lat'," Lat",block)
        block = re.sub('[a-zA-Z]\s+Lon'," Lon",block)
        block = re.sub('[a-zA-Z]\s+Nb'," Nb",block)
        block = re.sub('[a-zA-Z]\s+NOPC'," NOPC",block)
        block = re.sub('IQ',"#IQ",block)
        block = re.sub('[a-zA-Z]\s[a-zA-Z]',"O",block)

        split = '\#?[a-zA-Z0-9\-\>]+\s:\s'
        splitParameters = re.split(split,block)
        curDict = {}

        for i in range(len(splitParameters)) :
            if re.search('[?]+([a-zA-Z]+)?',splitParameters[i]) :
                splitParameters[i] = re.sub('[?]+([a-zA-Z]{1,2})?',"NaN",splitParameters[i])

            if re.search('[0-9]',splitParameters[i]):
                splitParameters[i] = re.sub('[a-zA-Z\s]'," ",splitParameters[i])

            if colsInBlock[i] == 'date' :
                curDict[colsInBlock[i]] = datetime.strptime(splitParameters[i],'%d.%m.%y %H:%M:%S ')
            else:
                try :
                    curDict[colsInBlock[i]] = int(splitParameters[i])   
                except :
                    try :
                        splitParameters[i] = re.sub('[\s]',"",splitParameters[i])
                        curDict[colsInBlock[i]] = float(splitParameters[i])
                    except :
                        curDict[colsInBlock[i]] = splitParameters[i]
        ListOfdictParams.append(curDict)

    df = pd.DataFrame.from_dict(ListOfdictParams)

    df = df.dropna(subset=['lat1', 'lon1','lat2', 'lon2','date'])
    DFToInsert = checkExistingArgos(df)
    DFToInsert['type']='arg'
    DFToInsert = DFToInsert.drop(['id','lat1','lat2','lon1','lon2'],1)

    data_to_insert = json.loads(DFToInsert.to_json(orient='records',date_format='iso'))

    if len(data_to_insert) != 0 :
        stmt = ArgosGps.__table__.insert()#.values(data_to_insert[0:2])
        res = DBSession.execute(stmt,data_to_insert)

    return len(data_to_insert)

def checkExistingArgos (dfToCheck) :

    dfToCheck['id'] = range(dfToCheck.shape[0])
    dfToCheck['lat'] = dfToCheck['lat1'].astype(float)
    dfToCheck['lon'] = dfToCheck['lon1'].astype(float)
    maxDate = dfToCheck['date'].max(axis=1)
    minDate = dfToCheck['date'].min(axis=1)

    queryArgos = select([ArgosGps.pk_id, ArgosGps.date, ArgosGps.lat, ArgosGps.lon, ArgosGps.ptt]).where(ArgosGps.type_ == 'arg')
    queryArgos = queryArgos.where(and_(ArgosGps.date >= minDate , ArgosGps.date <= maxDate))
    data = DBSession.execute(queryArgos).fetchall()

    ArgosRecords = pd.DataFrame.from_records(data
        ,columns=[ArgosGps.pk_id.name, ArgosGps.date.name, ArgosGps.lat.name, ArgosGps.lon.name, ArgosGps.ptt.name]
        , coerce_float=True )
    merge = pd.merge(dfToCheck,ArgosRecords, left_on = ['date','lat','lon','FK_ptt'], right_on = ['date','lat','lon','FK_ptt'])
    DFToInsert = dfToCheck[~dfToCheck['id'].isin(merge['id'])]

    return DFToInsert
