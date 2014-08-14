USE [ecoReleve_Data]
GO

/****** Object:  View [dbo].[V_Individuals_LatLonDate]    Script Date: 08/12/2014 16:38:30 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



-- =============================================
-- Author:		 Natural Solutions (Thomas PEEL)
-- Create date:  12/08/2014
-- Description:	 All stations of identified birds with station type
-- Modified on:  -
-- Modified by:  -
-- =============================================


CREATE view [dbo].[V_Individuals_LatLonDate] AS
SELECT ind_id, lat, lon, date
FROM V_Individuals_Stations
INNER JOIN TStations
	ON sta_id = TSta_PK_ID
WHERE LAT is not null AND LON is not null AND DATE is not null

GO