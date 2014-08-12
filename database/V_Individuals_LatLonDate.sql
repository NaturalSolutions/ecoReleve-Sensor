USE [ecoReleve_Data]
GO

/****** Object:  View [dbo].[VStations]    Script Date: 07/08/2014 16:42:57 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



--- Creation de la vue V_Individuals_LatLonDate
Create view [dbo].[V_Individuals_LatLonDate] as
select indID, lat, lon, date
from
(
	select FK_Tind_ID as indID, FK_TSta_ID as staID, 'Death' as staType
	from dbo.TProtocol_Vertebrate_Individual_Death

	union

	select FK_Tind_ID as indID, FK_TSta_ID as staID, 'Nest' as staType
	from dbo.TProtocol_Nest_Description
	
	union
	
	select FK_Tind_ID as indID, FK_TSta_ID as staID, 'Release' as staType
	from dbo.TProtocol_Release_Individual
	
	union
	
	select FK_Tind_ID as indID, FK_TSta_ID as staID, 'Capture' as staType
	from dbo.TProtocol_Capture_Individual
	
	union
	
	select FK_Tind_ID as indID, FK_TSta_ID as staID, 'GPS' as staType
	from dbo.TProtocol_ArgosDataGPS
	
	union
	
	select FK_Tind_ID as indID, FK_TSta_ID as staID, 'Argos' as staType
	from dbo.TProtocol_ArgosDataArgos
	
	union
	
	select FK_Tind_ID as indID, FK_TSta_ID as staID, 'Vertebrate Individual' as staType
	from dbo.TProtocol_Vertebrate_Individual
) t
inner join TStations on staID = TSta_PK_ID
where indID is not null and LAT is not null and LON is not null and DATE is not null

GO


