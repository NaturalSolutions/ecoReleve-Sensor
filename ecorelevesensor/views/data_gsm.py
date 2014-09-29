"""
Created on Tue Sep 23 17:15:47 2014

@author: Natural Solutions (Thomas)
"""

from pyramid.view import view_config
from sqlalchemy import desc, select, func
from ecorelevesensor.models import AnimalLocation, DBSession, DataGsm
from ecorelevesensor.utils.distance import haversine

import pandas as pd
import numpy as np

prefix = 'dataGsm/'

@view_config(route_name=prefix + 'unchecked/list', renderer='json')
def data_gsm_unchecked_list(request):
    '''List unchecked GSM data.
    '''
    query = select([
        DataGsm.platform_,
        func.count(DataGsm.id).label('nb')
    ]).group_by(DataGsm.platform_)
    return [dict(row) for row in DBSession.execute(query).fetchall()]

@view_config(route_name=prefix + 'unchecked', renderer='json')
def data_gsm_unchecked(request):
    '''Get the unchecked GSM data.
    '''
    platform = int(request.matchdict['id'])
    
    if request.GET['format'] == 'geojson':
        # Query
        query = select([
            DataGsm.id.label('id'),
            DataGsm.lat,
            DataGsm.lon,
            DataGsm.date_
        ]).where(DataGsm.platform_ == platform).where(DataGsm.checked == False).order_by(desc(DataGsm.date_))
        # Create list of features from query result
        features = [
            {
                'type':'Feature',
                'properties':{'date':str(date)},
                'geometry':{'type':'Point', 'coordinates':[float(lon),float(lat)]},
                'id':id_
            }
        for id_, lat, lon, date in DBSession.execute(query).fetchall()]
        result = {'type':'FeatureCollection', 'features':features}
        return result
        
    elif request.GET['format'] == 'json':
        # Query
        query = select([
            DataGsm.id.label('id'),
            DataGsm.lat,
            DataGsm.lon,
            DataGsm.ele,
            DataGsm.date_]
        ).where(DataGsm.platform_ == platform
        ).where(DataGsm.checked == False
        ).order_by(desc(DataGsm.date_))
        data = DBSession.execute(query).fetchall()
        # Load data from the DB then
        # compute the distance between 2 consecutive points.
        df = pd.DataFrame.from_records(data, columns=data[0].keys(), coerce_float=True)
        X1 = df.ix[:,['lat', 'lon']].values[:-1,:]
        X2 = df.ix[1:,['lat', 'lon']].values
        df['dist'] = np.append(haversine(X1, X2).round(3), 0)
        df['speed'] = (df['dist']/((df['date_']-df['date_'].shift(-1)).fillna(1)/np.timedelta64(1, 'h'))).round(3)
        df['import'] = [False]*len(df.index)
        ids = df.set_index('date_').resample('1H', how='first').dropna().id.values
        df['import'][df.id.isin(ids)] = True
        df['date_'] = df['date_'].apply(lambda d: str(d))
        return df.to_dict('records')
        
@view_config(route_name=prefix + 'unchecked/import', renderer='json')
def data_gsm_unchecked_import(request):
    '''Import unchecked GSM data.
    '''
    
    data = request.json_body.get('data')
    select_stmt = select(DataGsm)
    query = insert(AnimalLocation, select([DataGsm.__table__.c]))
    
    query = select([
        DataGsm.platform_,
        func.count(DataGsm.id).label('nb')
    ]).group_by(DataGsm.platform_)
    
    return [dict(row) for row in DBSession.execute(query).fetchall()]