-- =============================================
-- Author:		Romain FABBRO
-- Create date: 2015-02-27
-- Description: create procedure to auto validate GSM 1 data/hour
-- =============================================

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO



ALTER PROCEDURE [dbo].[sp_auto_validate_gsm]
	@ptt int,
	@ind int,
	@user int,
	@nb_insert int OUTPUT,
	@exist int OUTPUT,
	@error int OUTPUT


AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

	SET NOCOUNT ON;
	DECLARE @data_to_insert table ( 
		data_id int
		,platform_ int
		, date_ datetime
		, lat decimal(9,5)
		, lon decimal(9,5)
		,speed int
		,course int
		,ele int 
		,hdop numeric(3,1)
		,vdop numeric(3,1)
		,sat_count int
		, FK_ind int
		,creator int
		,name varchar(100)
		 );
	DECLARE @data_duplicate table ( 
		data_id int,
		fk_sta_id int
		);

	DECLARE @output TABLE (sta_id int,
							data_id int);

	DECLARE @NbINserted int;

	-- Gather not validated data.
	WITH data AS (
		SELECT *
			, ROW_NUMBER() OVER (PARTITION BY CONVERT(DATE, date_), DATEPART(hour, date_) ORDER BY date_) as r
		FROM V_dataGSM_with_IndivEquip where ind_id = @ind and ptt=@ptt and checked = 0 
	)


	INSERT INTO @data_to_insert (data_id,platform_,date_,lat,lon,speed,course,ele,hdop,vdop,sat_count,FK_ind,creator,name)
		SELECT 
		data_PK_ID
		,ptt
		,date_
		,lat
		,lon
		,Speed
		,Course
		,ele
		,HDOP
		,VDOP
		,sat_count
		,ind_id
		,@user
		,'ARGOS_'+CAST(ptt as varchar(55))+'_'+FORMAT(date_,'yyyyMMddHHmmss')
		FROM data
		WHERE data.r = 1;

	
	--check duplicate data into @data_without_duplicate  
	insert into  @data_duplicate 
	select d.data_id, s.TSta_PK_ID
	from @data_to_insert d join TStations s on d.lat=s.LAT and d.lon = s.LON and d.date_ = s.DATE and s.Name = d.name

	-- insert data creating new station and linked Tsta_PK_ID to data_id using FieldWorker1
	Insert into TStations (FieldActivity_ID,FieldActivity_Name,Name,DATE, LAT,LON,ELE,Creation_date, Creator,regionUpdate,FieldWorker1)
	output inserted.TSta_PK_ID,inserted.FieldWorker1 into @output
	select 
	27
	,'Automatic data acquisition'
	,'ARGOS_'+CAST(platform_ as varchar(55))+'_'+FORMAT(date_,'yyyyMMddHHmmss')
	,date_
	,lat
	,lon
	,ele
	,getdate()
	,creator
	,0
	,data_id
	from @data_to_insert where data_id not in (select data_id from @data_duplicate)
	SET @NbINserted=@@ROWCOUNT

	Insert into TProtocol_ArgosDataGPS (FK_TSta_ID,FK_TInd_ID,TADG_Course,TADG_Speed)
	select o.sta_id, FK_ind,course,speed
	FROM @data_to_insert i 
	join @output o on o.data_id=i.data_id
	where i.data_id not in (select data_id from @data_duplicate)

	update TStations set FieldWorker1= null where TSta_PK_ID in (select sta_id from @output)
	update T_DataGsm set validated = 1 where PK_id in (select data_id from @data_to_insert)
	update V_dataGSM_with_IndivEquip set checked = 1 where ptt = @ptt and ind_id = @ind

	SET @nb_insert=@NbINserted
	select @exist = COUNT(*) FROM @data_duplicate
	SET @error = @@ERROR

	return
End



GO


