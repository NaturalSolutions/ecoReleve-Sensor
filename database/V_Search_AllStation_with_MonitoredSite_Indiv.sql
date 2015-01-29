-- =============================================
-- Author:		Romain FABBRO
-- Create date: 2014-12-11
-- Description:	create View to search in all Station with monitored site and Individual ID
-- =============================================


USE [ecoReleve_Data]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

ALTER VIEW V_Search_AllStation_with_MonitoredSite_Indiv2
AS

SELECT  
sta.[TSta_PK_ID] as id
,sta.[NbFieldWorker] as nbFieldWorker
,sta.[FieldActivity_ID] as FieldActivity_ID
,sta.[FieldActivity_Name] as FieldActivity_Name
,sta.[Name] as Name
,sta.[Region] as Region
,sta.[Place] as Place
,sta.[DATE] as date
,sta.[LAT] as LAT
,sta.[LON] as LON
,sta.[Precision] as Precision
,sta.[ELE] as ELE
,sta.[Creator] as Creator
,sta.[Creation_date] as Creation_date
,sta.[TSta_FK_TGeo_ID] as site_id
,sta.[Id_DistanceFromObs] as Id_DistanceFromObs
,sta.[Name_DistanceFromObs] as Name_DistanceFromObs
,sta.[Comments] as Comments
,sta.[UTM20] as UTM20
,sta.[regionUpdate] as regionUpdate
,ind.ind_id as ind_id
,(u1.lastname+' '+u1.firstname) as FieldWorker1
,(u2.lastname+' '+u2.firstname) as FieldWorker2
,(u3.lastname+' '+u3.firstname) as FieldWorker3
, sta.FieldWorker1 FieldWorker1_ID, sta.FieldWorker2 FieldWorker2_ID, sta.FieldWorker3 FieldWorker3_ID
,m.name_Type as site_type
,m.Name as site_name

FROM TStations sta 
left outer join [dbo].[V_Individuals_Stations] ind ON sta.TSta_PK_ID= ind.sta_id
left outer join [dbo].[TMonitoredStations] m on sta.[TSta_FK_TGeo_ID]=m.TGeo_pk_id 
left outer join T_User_Full u1 on sta.FieldWorker1=u1.PK_id
left outer join T_User_Full u2 on sta.FieldWorker2=u2.PK_id
left outer join T_User_Full u3 on sta.FieldWorker3=u3.PK_id

GO