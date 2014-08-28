"""
Created on Tue Aug 26 17:36:11 2014

@author: Natural Solutions (Thomas)
"""

from pyramid.view import view_config

from sqlalchemy import func, desc, select, union_all, and_, bindparam, update, or_, literal

from ecorelevesensor.models import DBSession
from ecorelevesensor.models.sensor import Argos, Gps, Gsm
from ecorelevesensor.models.data import (
   Individuals,
   ProtocolArgos,
   ProtocolGps,
   ProtocolIndividualEquipment,
   SatTrx,
   Station,
   V_Individuals_LatLonDate
)

route_prefix = 'sensor/'

# List all PTTs having unchecked locations, with individual id and number of locations.
@view_config(
    route_name=route_prefix+'unchecked',
    permission='read',
    renderer='json')
def argos_unchecked_list(request):
    """Returns the unchecked sensor data summary.
    """
    # SQL query
    unchecked = union_all(
        select([
            Argos.pk,
            Argos.ptt.label('ptt'),
            Argos.date,
            literal('argos/gps').label('type')
        ]).where(Argos.checked == False),
        select([
            Gps.pk,
            Gps.ptt.label('ptt'),
            Gps.date,
            literal('argos/gps').label('type')
        ]).where(Gps.checked == False),
        select([
            Gsm.pk_id,
            Gsm.fk_ptt.label('ptt'),
            Gsm.date,
            literal('gsm').label('type')
        ]).where(Gsm.checked == False)
    ).alias()
    # Add the bird associated to each ptt.
    pie = ProtocolIndividualEquipment
    unchecked_with_ind = select([
        pie.ind_id.label('ind_id'),
        'ptt',
        func.count().label('count'),
        'type'
    ]).select_from(
        unchecked.join(SatTrx, SatTrx.ptt == unchecked.c.ptt)
        .outerjoin(
            pie,
            and_(SatTrx.id == pie.sat_id,
                 unchecked.c.date >= pie.begin_date,
                 or_(
                     unchecked.c.date < pie.end_date,
                     pie.end_date == None
                )
            )
        )
    ).group_by('ptt', 'type', pie.ind_id)#.order_by('ptt')
    # Populate Json array
    data = DBSession.execute(unchecked_with_ind).fetchall()
    return [dict(row) for row in data]