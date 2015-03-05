-- =============================================
-- Author:		Romain FABBRO
-- Create date: 2015-02-27
-- Description:	View for DataArgos_GPS with Individual equipment date 
-- =============================================


SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO





CREATE view [dbo].[V_dataGPS_with_IndivEquip]
as
SELECT 
[V_TProtocol_Individual_Equipement].[FK_IND_ID] AS ind_id,
[V_TProtocol_Individual_Equipement].begin_date AS begin_date,
[V_TProtocol_Individual_Equipement].end_date AS end_date,
gps.[PK_id] as data_PK_ID,
gps.[FK_ptt] as ptt ,
gps.[date] as date_,
gps.[lat] as lat,
gps.[lon] as lon,
gps.ele,
gps.speed,
gps.course,
gps.checked,
gps.imported

FROM [ecoReleve_Sensor].dbo.[Tgps] as gps
LEFT OUTER JOIN  [ecoReleve_DataNew].[dbo].[V_TProtocol_Individual_Equipement]  ON  gps.FK_ptt = [V_TProtocol_Individual_Equipement].ptt 
AND gps.[date] >= [V_TProtocol_Individual_Equipement].begin_date 
AND (gps.[date] < [V_TProtocol_Individual_Equipement].end_date OR [V_TProtocol_Individual_Equipement].end_date IS NULL)
WHERE ([V_TProtocol_Individual_Equipement].model_precision LIKE '%solar%' OR [V_TProtocol_Individual_Equipement].model_precision is null)






GO