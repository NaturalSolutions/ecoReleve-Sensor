/****** Object:  View [dbo].[V_dataGSM_with_IndivEquip]    Script Date: 13/02/2015 15:15:57 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE view [dbo].[V_dataGSM_with_IndivEquip]
as
SELECT [V_TProtocol_Individual_Equipement].[FK_IND_ID] AS ind_id,  [T_DataGsm].platform_  as ptt,
[V_TProtocol_Individual_Equipement].begin_date AS begin_date,
[V_TProtocol_Individual_Equipement].end_date AS end_date,
[T_DataGsm].Latitude_N as lat,
[T_DataGsm].Longitude_E as lon,
[T_DataGsm].Altitude_m as ele, 
[T_DataGsm].checked as checked,
[T_DataGsm].imported as imported,
[T_DataGsm].DateTime as date_,
[T_DataGsm].Course as course,
[T_DataGsm].HDOP as HDOP,
[T_DataGsm].Speed as speed,
[T_DataGsm].SatelliteCount as sat_count,
[T_DataGsm].VDOP as VDOP,
[T_DataGsm].validated as validated,
[T_DataGsm].PK_id as data_PK_ID

FROM [T_DataGsm]
LEFT OUTER JOIN  [V_TProtocol_Individual_Equipement]  ON  [T_DataGsm].platform_ = [V_TProtocol_Individual_Equipement].ptt 
AND [T_DataGsm].[DateTime] >= [V_TProtocol_Individual_Equipement].begin_date 
AND ([T_DataGsm].[DateTime] < [V_TProtocol_Individual_Equipement].end_date OR [V_TProtocol_Individual_Equipement].end_date IS NULL)
WHERE ([V_TProtocol_Individual_Equipement].model_precision LIKE 'GSM%' OR [V_TProtocol_Individual_Equipement].model_precision is null)


GO