-- =============================================
-- Author:		Romain FABBRO
-- Create date: 2014-12-09
-- Description:	complete TProtocol_Individual_Equipment table
-- =============================================

Insert into [TProtocol_Individual_Equipment]

SELECT Trx_Sat_Obj_PK,Individual_Obj_PK,begin_date,end_date
 FROM TViewTrx_Sat gsm
JOIN TObj_Carac_value obj ON gsm.id19@TCarac_PTT = CAST(obj.value as int)
JOIN TViewIndividual ind ON ind.Individual_Obj_PK = obj.fk_object
where Fk_carac = 19 AND object_type = 'Individual'