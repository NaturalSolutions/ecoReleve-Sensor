

/****** Object:  StoredProcedure [dbo].[sp_GetRegionFromLatLon]    Script Date: 23/02/2015 16:31:26 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


-- =============================================
-- Author:		Thomas Peel
-- Create date: 2014-04-13
-- Description:	Return the region the point given in parameter is inside.
-- =============================================
CREATE PROCEDURE [dbo].[sp_GetRegionFromLatLon] 
	-- Add the parameters for the stored procedure here
	@lat decimal(9,5) = null, 
	@lon decimal(9,5) = null,
	@geoPlace varchar(255) = null OUTPUT
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
	
	-- Transforms lat and lon to a geometry object
	declare @point geometry;
	set @point = geometry::STPointFromText('Point(' + CONVERT(varchar, @lon) + ' ' + CONVERT(varchar, @lat) +')', 4326);

    -- Select the Place the point is inside
	SELECT @geoPlace = Place FROM geo_CNTRIES_and_RENECO_MGMTAreas WHERE @point.STWithin(valid_geom) = 1
END
GO


-- =============================================
-- Author:		Thomas Peel
-- Create date: 2014-04-13
-- Description:	Return the code of the plot the point given in parameter is inside.
-- =============================================
CREATE PROCEDURE [dbo].[sp_GetUTMCodeFromLatLon] 
	-- Add the parameters for the stored procedure here
	@lat decimal(9,5) = null, 
	@lon decimal(9,5) = null,
	@geoPlace varchar(255) = null OUTPUT
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
	
	-- Transforms lat and lon to a geometry object
	declare @point geometry;
	set @point = geometry::STPointFromText('Point(' + CONVERT(varchar, @lon) + ' ' + CONVERT(varchar, @lat) +')', 4326);

    -- Select the Place the point is inside
	SELECT @geoPlace = code FROM geo_utm_grid_20x20_km WHERE @point.STWithin(ogr_geometry) = 1
END
GO
