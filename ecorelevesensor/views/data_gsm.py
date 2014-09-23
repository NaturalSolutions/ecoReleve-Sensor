"""
Created on Tue Sep 23 17:15:47 2014

@author: Natural Solutions (Thomas)
"""

from pyramid.view import view_config
from sqlalchemy import desc, select
from ecorelevesensor.models import DBSession, DataGsm

prefix = 'dataGsm/'

@view_config(route_name=prefix + 'unchecked', renderer='json')
def data_gsm_unchecked(request):
    '''Get the unchecked GSM data.
    '''
    gsm = int(request.matchdict['id'])
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
            'properties':{'date':str(date), 'id':id_},
            'geometry':{'type':'Point', 'coordinates':[float(lon),float(lat)]}
        }
    for id_, lat, lon, date in DBSession.execute(query).fetchall()]
    result = {'type':'FeatureCollection', 'features':features}
    return result