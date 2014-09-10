USE [ecoReleve_Data]
GO

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

ALTER VIEW [dbo].[V_Individuals_Stations] as
select ind_id, sta_id, fk_sta_type
from
(
	select FK_Tind_ID as ind_id, FK_TSta_ID as sta_id, 1 as fk_sta_type
	from dbo.TProtocol_Vertebrate_Individual_Death

	union all

	select FK_Tind_ID as ind_id, FK_TSta_ID as sta_id, 2 as fk_sta_type
	from dbo.TProtocol_Nest_Description
	
	union all
	
	select FK_Tind_ID as ind_id, FK_TSta_ID as sta_id, 3 as fk_sta_type
	from dbo.TProtocol_Release_Individual
	
	union all
	
	select FK_Tind_ID as ind_id, FK_TSta_ID as sta_id, 4 as fk_sta_type
	from dbo.TProtocol_Capture_Individual
	
	union all
	
	select FK_Tind_ID as ind_id, FK_TSta_ID as sta_id, 5 as fk_sta_type
	from dbo.TProtocol_ArgosDataGPS
	
	union all
	
	select FK_Tind_ID as ind_id, FK_TSta_ID as sta_id, 6 as fk_sta_type
	from dbo.TProtocol_ArgosDataArgos
	
	union all
	
	select FK_Tind_ID as ind_id, FK_TSta_ID as sta_id, 7 as fk_sta_type
	from dbo.TProtocol_Vertebrate_Individual
) t
WHERE ind_id IS NOT NULL

GO