/****** Object:  View [dbo].[V_TProtocol_Individual_Equipement]    Script Date: 13/02/2015 15:16:03 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE View [dbo].[V_TProtocol_Individual_Equipement]
as 
SELECT SatTrx.Trx_Sat_Obj_PK as FK_SAT_ID
,SatTrx.id19@TCarac_PTT as ptt
,ind.Individual_Obj_PK as FK_IND_ID
,ObjectsCaracValues.begin_date as begin_date
,ObjectsCaracValues.end_date as end_date
, SatTrx.id41@TCaracThes_Model_Precision as model_precision



FROM TViewTrx_Sat SatTrx JOIN TObj_Carac_value ObjectsCaracValues ON SatTrx.id19@TCarac_PTT = CAST(ObjectsCaracValues.value as INT) 
join TViewIndividual ind ON  ObjectsCaracValues.fk_object =ind.Individual_Obj_PK
where 
ObjectsCaracValues.Fk_carac=19 
and ObjectsCaracValues.object_type = 'Individual'
GO