USE [ecoReleve_DataNew]
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