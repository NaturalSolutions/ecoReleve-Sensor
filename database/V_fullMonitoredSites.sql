SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		Romain FABBRO
-- Create date: 2015-02-09
-- Description:	
-- =============================================




ALTER VIEW dbo.V_fullMonitoredSites 
AS

SELECT s.Name as name
,s.Creation_date as creation_date
,s.name_Type as type
, p.TGeoPos_LAT as lat 
,p.TGeoPos_LON as lon
,p.TGeoPos_ELE as ele
,p.TGeoPos_Begin_Date as begin_date
,p.TGeoPos_End_Date as end_date
,s.Active as active
,s.TGeo_pk_id as id

FROM [dbo].[TMonitoredStations] s  join TMonitoredStations_Positions p on s.TGeo_pk_id=p.TGeoPos_FK_TGeo_ID