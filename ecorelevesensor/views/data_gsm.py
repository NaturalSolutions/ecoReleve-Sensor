"""
Created on Tue Sep 23 17:15:47 2014

@author: Natural Solutions (Thomas)
"""

from pyramid.view import view_config
from sqlalchemy import desc, select
from ecorelevesensor.models import DBSession, DataGsm
from ecorelevesensor.utils.distance import haversine

import pandas as pd
import numpy as np

prefix = 'dataGsm/'

@view_config(route_name=prefix + 'unchecked', renderer='json')
def data_gsm_unchecked(request):
    '''Get the unchecked GSM data.
    '''
    gsm = int(request.matchdict['id'])
    
    if request.GET['format'] == 'geojson':
        # Query
        query = select([
            DataGsm.id.label('id'),
            DataGsm.lat,
            DataGsm.lon,
            DataGsm.date_
        ]).where(DataGsm.gsm == gsm).where(DataGsm.checked == False).order_by(desc(DataGsm.date_))
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
            DataGsm.date_
        ]).where(DataGsm.gsm == gsm).where(DataGsm.checked == False).order_by(desc(DataGsm.date_))
        data = DBSession.execute(query).fetchall()
        # Load data from the DB then
        # compute the distance between 2 consecutive points.
        df = pd.DataFrame.from_records(data, columns=data[0].keys(), coerce_float=True)
        X1 = df.ix[:,['lat', 'lon']].values[:-1,:]
        X2 = df.ix[1:,['lat', 'lon']].values
        dist = pd.Series(np.append(haversine(X1, X2).round(3), 0), name='dist')
        impo = pd.Series([False]*len(data), name='import')
        df = pd.concat([df['id'], df['date_'].apply(lambda x: str(x)), df['lat'], df['lon'], dist, impo], axis=1)
        return df.to_dict('records')