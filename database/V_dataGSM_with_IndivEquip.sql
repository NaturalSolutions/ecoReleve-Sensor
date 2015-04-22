
-- =============================================
-- Author:		Romain FABBRO
-- Create date: 2015-02-02
-- Description:	View for DataGSM with Individual equipment date 
-- =============================================


--Les données ne doivent pas etre montrées si elles présentent au moins une des conditions suivantes,
--       permettant d'estimer la qualité des positions :
---   VDOP < 1 et VDOP > 10 (Vertical Dilution Of Precision = précision verticale)
---   HDOP < 6 (Horizontal Dilution Of Precision = précision horizontale)
---   Nombre de satellites < 5

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


ALTER view [dbo].[V_dataGSM_with_IndivEquip]
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
AND ([T_DataGsm].[DateTime] <= [V_TProtocol_Individual_Equipement].end_date OR [V_TProtocol_Individual_Equipement].end_date IS NULL)
WHERE ([V_TProtocol_Individual_Equipement].model_precision LIKE 'GSM%' OR [V_TProtocol_Individual_Equipement].model_precision is null)
AND (T_DataGsm.HDOP >= 6 
OR T_DataGsm.VDOP BETWEEN 1 AND 10 
OR T_DataGsm.SatelliteCount >=5 )


GO



