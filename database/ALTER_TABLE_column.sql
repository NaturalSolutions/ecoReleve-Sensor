  ALTER TABLE [dbo].[TProtocol_Chiroptera_capture] 
  ADD hours time(2)

  GO

  UPDATE [ecoReleve_DataNew].[dbo].[TProtocol_Chiroptera_capture] SET hours=Hour

  GO

  ALTER TABLE [dbo].[TProtocol_Chiroptera_capture] 
  DROP COLUMN HOUR