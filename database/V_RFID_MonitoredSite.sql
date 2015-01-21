USE [ECWP-eReleveData]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		Romain FABBRO
-- Create date: 2014-11-20
-- Description:	
-- =============================================

create view [dbo].[RFID_MonitoredSite]
 AS
SELECT obj.*,eq.lat, eq.lon,eq.begin_date,eq.end_date, MS.name_Type,MS.Name
FROM T_Object obj JOIN  [T_MonitoredSiteEquipment] eq ON obj.PK_id=eq.FK_obj
JOIN [dbo].[TMonitoredStations] MS ON eq.FK_site=MS.TGeo_pk_id 
GO

-- UPDATE VIEW --

ALTER view [dbo].[RFID_MonitoredSite]
 AS
SELECT obj.*, obj.PK_id as PK_obj,eq.PK_id as PK_equio, eq.lat, eq.lon,eq.begin_date,eq.end_date,MS.TGeo_pk_id as PK_site, MS.name_Type,MS.Name
FROM T_Object obj left outer JOIN  [T_MonitoredSiteEquipment] eq ON obj.PK_id=eq.FK_obj
left outer JOIN [dbo].[TMonitoredStations] MS ON eq.FK_site=MS.TGeo_pk_id 
where obj.type_='rfid'

GO

--