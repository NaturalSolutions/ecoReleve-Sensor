-- =============================================
-- Author:		Romain FABBRO
-- Create date: 2015-02-20
-- Description:	alter table TProtocol_Phytosociology_releve recreate column to stock thesaurus full-path
-- =============================================

  
  Alter table [dbo].[TProtocol_Phytosociology_releve] 
  ADD Name_Global_Abondance_Dom_2 nvarchar(250) null,
  Name_Global_Sociability_2 nvarchar(250) null,
  Name_Phenology_BBCH1_2 nvarchar(250) null,
  Name_Phenology_BBCH2_2 nvarchar(250) null

  GO 

  update [dbo].[TProtocol_Phytosociology_releve] 
  Set 
  Name_Global_Abondance_Dom_2 = Name_Global_Abondance_Dom,
  Name_Global_Sociability_2 = Name_Global_Sociability,
  Name_Phenology_BBCH1_2 = Name_Phenology_BBCH1,
  Name_Phenology_BBCH2_2 = Name_Phenology_BBCH2
  
  GO 

  Alter table [dbo].[TProtocol_Phytosociology_releve] 
  DROP COLUMN Name_Global_Abondance_Dom,Name_Global_Sociability,Name_Phenology_BBCH1,Name_Phenology_BBCH2

GO
EXEC sp_rename 'TProtocol_Phytosociology_releve.Name_Global_Abondance_Dom_2', 'Name_Global_Abondance_Dom', 'COLUMN';
GO
EXEC sp_rename 'TProtocol_Phytosociology_releve.Name_Global_Sociability_2', 'Name_Global_Sociability', 'COLUMN';
GO 
EXEC sp_rename 'TProtocol_Phytosociology_releve.Name_Phenology_BBCH1_2', 'Name_Phenology_BBCH1', 'COLUMN';
GO 
EXEC sp_rename 'TProtocol_Phytosociology_releve.Name_Phenology_BBCH2_2', 'Name_Phenology_BBCH2', 'COLUMN';
GO 