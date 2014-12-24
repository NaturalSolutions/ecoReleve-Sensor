-- =============================================
-- Author:		Romain FABBRO
-- Create date: 2014-12-23
-- Description:	alter table Data sensors
-- =============================================



USE [ecoReleve_Data]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

ALTER TABLE dbo.T_DataRfid 
ADD checked BIT,frequency_hour numeric (5,3) 

GO

ALTER TABLE dbo.T_DataGsm
ADD validated BIT

GO

ALTER TABLE dbo.T_AnimalLocation
ADD frequency_hour numeric (5,3) 

GO