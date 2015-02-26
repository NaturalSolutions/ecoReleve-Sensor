-- =============================================
-- Author:		Romain FABBRO
-- Create date: 2015-02-26
-- Description: create procedure to checked=True in T_dataGSM for all data with xml
-- =============================================


SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



create PROCEDURE [dbo].[sp_check_gsm_byXML]
	@listID xml
	
	
AS
BEGIN
    
	SET NOCOUNT ON;

update T_DataGsm set checked = 1 
where PK_id in 
(
select * from [dbo].[XML_extractID_1] (@listID)
)


RETURN
END




GO