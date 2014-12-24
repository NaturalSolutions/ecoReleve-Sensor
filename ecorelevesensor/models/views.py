from sqlalchemy import (
    and_,
    desc,
    func,
    join,
    outerjoin,
    select,
    union,
    union_all,
    bindparam, update, or_, literal_column
)

from ecorelevesensor.models.sensor import Argos, Gps
from .individual import Individual
from ecorelevesensor.models.data import (
    ProtocolArgos,
    ProtocolGps,
    ProtocolIndividualEquipment,
    # ProtocolCaptureIndividual,
    # ProtocolReleaseIndividual,
    SatTrx,
    Station
)
from ecorelevesensor.models import (TProtocolCaptureIndividual,TProtocolReleaseIndividual)



ReleaseSta = select([
    Station.area.label('release_area'),
    func.year(Station.date).label('release_year'),
    TProtocolReleaseIndividual.FK_TInd_ID.label('ind_id'),
    TProtocolCaptureIndividual.Id_Observer.label('Id_Observer'),
    TProtocolReleaseIndividual.Comments.label('comments_Release'),
    TProtocolCaptureIndividual.Comments.label('comments_Capture')
    ]).select_from(join(Station, TProtocolReleaseIndividual,
        TProtocolReleaseIndividual.FK_TSta_ID == Station.id
    ).outerjoin(TProtocolCaptureIndividual, 
    TProtocolCaptureIndividual.FK_TInd_ID == TProtocolReleaseIndividual.FK_TInd_ID )).alias()

V_SearchIndiv = select([
    Individual.id.label('id'),
    Individual.chip_code.label('chip_code'),
    Individual.breeding_ring.label('breeding_ring'),
    Individual.release_ring.label('release_ring'),
    Individual.age.label('age'),
    Individual.mark1.label('mark1'),
    Individual.mark2.label('mark2'),
    Individual.monitoring_status.label('monitoring_status'),
    Individual.origin.label('origin'),
    Individual.ptt.label('ptt'),
    Individual.frequency.label('frequency'),
    Individual.sex.label('sex'),
    Individual.species.label('species'),
    Individual.status.label('status'),
    Individual.survey_type.label('survey_type'),
    ReleaseSta.c['release_area'],
    ReleaseSta.c['release_year'],
    ReleaseSta.c['Id_Observer'],
    ReleaseSta.c['comments_Release'],
    ReleaseSta.c['comments_Capture'],

]).select_from(
    outerjoin(Individual, ReleaseSta, ReleaseSta.c['ind_id']==Individual.id)).alias()
"""
id5@TCarac_Transmitter_Frequency as frequency,
id8@TCaracThes_Release_Ring_Color_Precision as releaseRingColor,
id14@TCaracThes_Mark_Color_1_Precision as markColor1,
id60@TCaracThes_Monitoring_Status_Precision as monitoringStatus,
id61@TCaracThes_Survey_type_Precision as surveyType,
capt.Area as captureArea,
YEAR(capt.Date) as captureYear

	(select FK_TInd_ID, Area, Date
	from [ecoReleve_Data].[dbo].[TProtocol_Release_Individual]
	inner join [ecoReleve_Data].[dbo].TStations
	on FK_TSta_ID = TSta_PK_ID) rel
	on rel.FK_TInd_ID = Individual_Obj_PK
	left outer join
	(select FK_TInd_ID, Area, Date
	from [ecoReleve_Data].[dbo].[TProtocol_Capture_Individual]
	inner join [ecoReleve_Data].[dbo].TStations
	on FK_TSta_ID = TSta_PK_ID) capt
	on capt.FK_TInd_ID = Individual_Obj_PK

GO
"""

# V_SearchIndiv_export = select([
#     Individual.id.label('id'),
#     Individual.chip_code.label('chip_code'),
#     Individual.breeding_ring.label('breeding_ring'),
#     Individual.release_ring.label('release_ring'),
#     Individual.age.label('age'),
#     Individual.birth_date('birth_date'),
#     Individual.mark1.label('mark1'),
#     Individual.mark2.label('mark2'),
#     Individual.monitoring_status.label('monitoring_status'),
#     Individual.origin.label('origin'),
#     Individual.ptt.label('ptt'),
#     Individual.frequency.label('frequency'),
#     Individual.sex.label('sex'),
#     Individual.species.label('species'),
#     Individual.status.label('status'),
#     Individual.survey_type.label('survey_type'),
#     ReleaseSta.c['release_area'],
#     ReleaseSta.c['release_year']
# ]).select_from(
#     outerjoin(Individual, ReleaseSta, ReleaseSta.c['ind_id']==Individual.id)).alias()