USE [ecoReleve_Data]
GO

/****** Object:  View [dbo].[V_Search_Indiv]    Script Date: 06/09/2014 11:28:12 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO





-- Modification de la vue V_Qry_AllIndivs_FirstStation
CREATE VIEW [dbo].[V_Search_Indiv] as
SELECT
Individual_Obj_PK as id,
id2@Thes_Age_Precision as age,
id5@TCarac_Transmitter_Frequency as frequency,
id8@TCaracThes_Release_Ring_Color_Precision as releaseRingColor,
id9@TCarac_Release_Ring_Code as releaseRingCode,
id12@TCarac_Breeding_Ring_Code as breedingRingCode,
id13@TCarac_Chip_Code as chipCode,
id14@TCaracThes_Mark_Color_1_Precision as markColor1,
id19@TCarac_PTT as ptt,
id30@TCaracThes_Sex_Precision as sex,
id33@Thes_Origin_Precision as origin,
id34@TCaracThes_Species_Precision as specie,
id60@TCaracThes_Monitoring_Status_Precision as monitoringStatus,
id61@TCaracThes_Survey_type_Precision as surveyType,
rel.Area as releaseArea,
YEAR(rel.date) as releaseYear,
capt.Area as captureArea,
YEAR(capt.Date) as captureYear

FROM
	[ecoReleve_Data].[dbo].TViewIndividual
	left outer join 
	(select FK_TInd_ID, Area, Date
	from [ecoReleve_Data].[dbo].[TProtocol_Release_Individual]
	inner join [ecoReleve_Data].[dbo].TStations
	on FK_TSta_ID = TSta_PK_ID) rel
	on rel.FK_TInd_ID = Individual_Obj_PK
	left outer join
	(select FK_TInd_ID, Area, Date
	from [ecoReleve_Data].[dbo].[TProtocol_Capture_Individual]
	inner join [ecoReleve_Data].[dbo].TStations
	on FK_TSta_ID = TSta_PK_ID) capt
	on capt.FK_TInd_ID = Individual_Obj_PK

GO


