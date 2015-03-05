
-- =============================================
-- Author:		Romain FABBRO
-- Create date: 2015-03-04
-- Description:	stored procedure for Argos_GPS manual validation  
-- =============================================

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO




CREATE PROCEDURE [dbo].[sp_validate_gps]
	@listID xml,
	@ind int,
	@user int,
	@ptt int , 
	@nb_insert int OUTPUT,
	@exist int output,
	@error int output
	
	
AS
BEGIN
   
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
		, FK_ind int
		,creator int
		 );

	DECLARE @data_duplicate table ( 
		data_id int,
		fk_sta_id int
		);

	DECLARE @output TABLE (sta_id int,
							data_id int);
	DECLARE @NbINserted int ; 

INSERT INTO @data_to_insert (data_id,platform_,date_,lat,lon,speed,course,ele,FK_ind,creator)
SELECT 
PK_id
,FK_ptt
,date
,lat
,lon
,Speed
,Course
,ele
,@ind
,@user
FROM ecoreleve_sensor.dbo.Tgps WHERE PK_id in (
select * from [dbo].[XML_extractID_1] (@listID)
) and checked = 0

-- check duplicate station before insert data in @data_without_duplicate
insert into  @data_duplicate  
select d.data_id, s.TSta_PK_ID
from @data_to_insert d join TStations s on d.lat=s.LAT and d.lon = s.LON and d.date_ = s.DATE


-- insert data creating new station and linked Tsta_PK_ID to data_id using FieldWorker1
Insert into TStations (FieldActivity_ID,FieldActivity_Name,Name,DATE, LAT,LON,ELE,Creation_date, Creator,regionUpdate, FieldWorker1)
output inserted.TSta_PK_ID,inserted.FieldWorker1 into @output
select 
27
,'Automatic data acquisition'
,'ARGOS_'+CAST(platform_ as varchar(55))+'_'+CONVERT(VARCHAR(24),date_,112)
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
update ecoreleve_sensor.dbo.Tgps set imported = 1 where PK_id in (select data_id from @data_to_insert)
update V_dataGPS_with_IndivEquip set checked = 1 where ptt = @ptt and ind_id = @ind

SET @nb_insert = @NbINserted
SELECT @exist = COUNT(*) FROM @data_duplicate
SET @error=@@ERROR

RETURN
END






GO


