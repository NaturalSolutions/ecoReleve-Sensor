"""
Created on Thu Aug 28 16:45:25 2014

@author: Natural Solutions (Thomas)
"""

import re

from pyramid.view import view_config
from sqlalchemy import select, insert, text, update, or_
from sqlalchemy.exc import IntegrityError

from ecorelevesensor.models import DBSession, MonitoredSite, MonitoredSitePosition
from ecorelevesensor.models import MonitoredSiteEquipment
from ecorelevesensor.models.object import ObjectRfid
from ecorelevesensor.utils.datetime import parse

prefix = 'monitoredSiteEquipment/'

@view_config(route_name=prefix+'pose', renderer='string', request_method='POST')
def monitored_site_equipment_pose(request):
    t = MonitoredSiteEquipment
    pose_info = request.POST
    print('______________pose info --------------')
    print (pose_info)
    creator= request.authenticated_userid
    values = {t.creator.name:creator}
    obj = DBSession.query(ObjectRfid.id).filter(ObjectRfid.identifier==pose_info['identifier']).scalar()
    site = DBSession.execute(select([MonitoredSite.id]
            ).where(MonitoredSite.type_==pose_info['type']
            ).where(MonitoredSite.name==pose_info['name'])).scalar()
    begin_date = parse(request.POST['begin'])
    if(pose_info['action'] == 'pose'):
        stmt = insert(MonitoredSiteEquipment)
        message = '1 row inserted'
        values[t.obj.name] = obj
        values[t.site.name] = site
        values[t.begin_date.name] = begin_date
        lat, lon = DBSession.execute(select([MonitoredSitePosition.lat, MonitoredSitePosition.lon]).where(
            MonitoredSitePosition.site == site).where(MonitoredSitePosition.end_date == None)).fetchone()
        values[t.lat.name] = lat
        values[t.lon.name] = lon
        values[t.end_date.name] = parse(pose_info['end'])
    elif(pose_info['action'] == 'remove'):
        stmt = update(MonitoredSiteEquipment
            ).where(MonitoredSiteEquipment.obj==obj
            ).where(MonitoredSiteEquipment.site==site)
        message = '1 row updated'
        d = parse(pose_info['end'])
        if d is not None:
            values[t.end_date.name] = d
        else:
            request.response.status_code = 500
            return 'Nothing to update'
    else:
        request.response.status_code = 500
        return 'Unknown action'
    try:
        DBSession.execute(stmt, values)
    except IntegrityError as e:
        request.response.status_code = 500
        return e
    return message