USE [ecoReleve_eReleve]
GO

/****** Object:  StoredProcedure [dbo].[sp_validate_rfid]    Script Date: 19/03/2015 20:28:52 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO




-- =============================================
-- Author:		Thomas PEEL
-- Create date: 2014-09-04
-- Description:	
-- =============================================
ALTER PROCEDURE [dbo].[sp_validate_rfid]
	@checked bit,
	@frequency_hour int,
	@user int,
	@nb int OUTPUT,
	@exist int output,
	@error int OUTPUT
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

	DECLARE @data_to_insert table ( PK_id int
		, FK_ind int
		, FK_obj int
		, chip_code varchar(10)
		, date_ datetime
		, lat decimal(9,5)
		, lon decimal(9,5)
		,freq int );

	DECLARE @data_duplicate table ( 
		data_id int,
		fk_loc_id int
		);
	-- Gather not validated data.
	WITH data AS (
		SELECT PK_id
			, FK_obj
			, chip_code
			, date_
			, validated
			,checked
			, ROW_NUMBER() OVER (PARTITION BY FK_obj, chip_code, CONVERT(DATE, date_), DATEPART(hour, date_) ORDER BY date_) as r
		FROM T_DataRfid
	)

	INSERT INTO @data_to_insert
    SELECT data.PK_id
		, indiv.Individual_Obj_PK
		, data.FK_obj
		, data.chip_code
		, date_
		, lat
		, lon
		,data.r
    FROM data
	JOIN TViewIndividual indiv 
		ON data.chip_code = indiv.id13@TCarac_Chip_Code
	JOIN T_MonitoredSiteEquipment e 
		ON e.FK_obj = data.FK_obj 
		AND data.date_ >= e.begin_date
		AND (data.date_ <= e.end_date OR e.end_date IS NULL)
	WHERE data.r = 1 AND data.validated = 0 and data.checked=@checked;

insert into  @data_duplicate  
select d.PK_id, s.PK_ID
from @data_to_insert d 
join T_AnimalLocation s ON d.FK_ind = a.FK_ind and d.date_ = a.date_ and d.FK_obj = a.FK_obj


	-- Insert only the first chip lecture per RFID, per individual, per hour.
	INSERT INTO T_AnimalLocation (FK_creator, FK_obj, FK_ind, type_, date_, lat, lon, creation_date, frequency_hour)
	SELECT @user, FK_obj, FK_ind, 'rfid', date_, lat, lon, CURRENT_TIMESTAMP, freq
	FROM @data_to_insert where PK_id not in (select data_id from @data_duplicate)

	-- Update inserted data.
	UPDATE T_DataRfid SET validated = 1 , frequency_hour= @frequency_hour
	WHERE T_DataRfid.PK_id IN (SELECT PK_id FROM @data_to_insert);
	UPDATE T_DataRfid SET checked = 1
	

	
	SELECT @error = @@ERROR
	SELECT @nb = COUNT(*) FROM @data_to_insert where not PK_id in (select data_id from @data_duplicate)
	SELECT @exist = COUNT(*) from @data_duplicate
	
	RETURN
END



GO


