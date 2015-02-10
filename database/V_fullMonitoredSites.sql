SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		Romain FABBRO
-- Create date: 2015-02-09
-- Description:	
-- =============================================




CREATE VIEW dbo.V_fullMonitoredSites 
AS

SELECT s.Name as name
,s.Creation_date as creation_date
,s.name_Type as type
, p.TGeoPos_ELE as lat 
,p.TGeoPos_LON as lon
,p.TGeoPos_ELE as ele
,p.TGeoPos_Begin_Date as begin_date
,p.TGeoPos_End_Date as end_date
,s.Active as active

FROM [ecoReleve_DataNew].[dbo].[TMonitoredStations] s  join TMonitoredStations_Positions p on s.TGeo_pk_id=p.TGeoPos_FK_TGeo_ID