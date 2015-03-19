-- =============================================
-- Author:		Romain FABBRO
-- Create date: 2015-02-20
-- Description:	View for DataArgos_GPS with Individual equipment date 
-- =============================================

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO




create view [dbo].[V_dataARGOS_GPS_with_IndivEquip]
as

(
SELECT
[V_TProtocol_Individual_Equipement].[FK_IND_ID] AS ind_id,
[V_TProtocol_Individual_Equipement].begin_date AS begin_date,
[V_TProtocol_Individual_Equipement].end_date AS end_date,
argos.[PK_id] as data_PK_ID,
argos.[FK_ptt] as ptt ,
argos.type as type_,
argos.[date] as date_,
argos.[lat] as lat,
argos.[lon] as lon,
argos.[lc] ,
argos.[iq] ,
argos.[ele] as ele,
argos.[speed],
argos.[course],
argos.[nbMsg] ,
argos.[nbMsg120] ,
argos.[bestLevel] ,
argos.[passDuration] ,
argos.[nopc] ,
argos.[freq] ,
argos.[errorRadius] ,
argos.[semiMajor]  ,
argos.[semiMinor]  ,
argos.[orientation],
argos.[hdop] ,
argos.[checked] ,
argos.[imported] 

FROM [ecoReleve_Sensor].dbo.[T_argosgps] as argos
LEFT OUTER JOIN  [V_TProtocol_Individual_Equipement]  ON  argos.FK_ptt = [V_TProtocol_Individual_Equipement].ptt 
AND argos.[date] >= [V_TProtocol_Individual_Equipement].begin_date 
AND (argos.[date] < [V_TProtocol_Individual_Equipement].end_date OR [V_TProtocol_Individual_Equipement].end_date IS NULL)
WHERE ([V_TProtocol_Individual_Equipement].model_precision LIKE '%solar%' OR [V_TProtocol_Individual_Equipement].model_precision is null)


)

