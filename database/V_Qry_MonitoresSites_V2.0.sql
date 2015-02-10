SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO





CREATE View [dbo].[V_Qry_MonitoredSites_V2] as
SELECT  CASE 
		WHEN RIGHT(YEAR(CURRENT_TIMESTAMP), 2) = LEFT(NAME, 2) THEN COALESCE(STUFF(NAME, CHARINDEX(RIGHT(YEAR(CURRENT_TIMESTAMP), 2),NAME), 2, 'z'),NAME ) 
		ELSE name
	END	AS name, 
	[name_Type] as type
	, TGeoPos_Begin_Date AS date
	, TMonitoredStations_Positions.TGeoPos_LAT as lat
	, TMonitoredStations_Positions.TGeoPos_LON as lon
	, TMonitoredStations_Positions.TGeoPos_ELE as ele
	, TMonitoredStations.TGeo_pk_id as id
	, TMonitoredStations_Positions.TGeoPos_Begin_Date as begin_date 
	, TMonitoredStations_Positions.TGeoPos_End_Date as end_date 
	,Active
FROM TMonitoredStations_Positions INNER JOIN TMonitoredStations ON TMonitoredStations_Positions.TGeoPos_FK_TGeo_ID = TMonitoredStations.TGeo_pk_id




GO
