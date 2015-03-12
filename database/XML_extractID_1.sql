-- =============================================
-- Author:		Romain FABBRO
-- Create date: 2015-03-03
-- Description:	function which receive an xml and transform it into table 
-- =============================================


SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE FUNCTION [dbo].[XML_extractID_1] ( @Xml xml )
RETURNS @DT TABLE
(
ID int
)
AS
BEGIN
INSERT INTO @DT (ID) 
SELECT ParamValues.ID.value('.','int')
FROM @xml.nodes('/table/row') as ParamValues(ID) 
RETURN
END


GO


