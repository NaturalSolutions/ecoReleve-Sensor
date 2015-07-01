-- =============================================
-- Author:		Romain FABBRO
-- Create date: 2015-03-19
-- Description:	stored procedure for all Argos (argos/GPS) auto validation 1/hour/type
-- =============================================

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO




ALTER PROCEDURE [dbo].[sp_auto_validate_argosArgos_argosGPS]
	@ptt int , 
	@ind int,
	@user int,
	@nb_insert int OUTPUT,
	@exist int output, 
	@error int output
	
	
AS
BEGIN
   
	SET NOCOUNT ON;
	DECLARE @data_to_insert table ( 
		data_id int,platform_ int, date_ datetime, lat decimal(9,5), lon decimal(9,5)
		, lc varchar(1), iq tinyint,ele int , nbMsg tinyint, nbMsg120dB tinyint
		, bestLevel smallint, passDuration	smallint,nopc tinyint,freq float
		,errorRadius int,semiMajor int,semiMinor int,orientation tinyint,hdop int , 
		speed int,course int, type_ varchar(3),
		 FK_ind int,creator int,name varchar(100)
		 );

	DECLARE @data_duplicate table ( 
		data_id int,fk_sta_id int
		);

	DECLARE @output TABLE (sta_id int,data_id int,type_ varchar(3));
	DECLARE @NbINserted int ; 

WITH data AS (
		SELECT data_PK_ID
			, ROW_NUMBER() OVER (PARTITION BY CONVERT(DATE, date_), DATEPART(hour, date_), type_ ORDER BY date_) as r
		FROM V_dataARGOS_GPS_with_IndivEquip where ind_id = @ind and ptt=@ptt and checked = 0 
	)


INSERT INTO @data_to_insert (data_id ,platform_ , date_ , lat , lon , lc , iq ,ele  ,
 nbMsg , nbMsg120dB , bestLevel , passDuration	,nopc ,freq ,
 errorRadius ,semiMajor ,semiMinor ,orientation ,hdop
 ,speed,course ,type_,
  FK_ind ,creator,name )
SELECT 
[PK_id],[FK_ptt],[date],[lat],[lon],[lc],[iq],[ele]
,[nbMsg],[nbMsg120],[bestLevel],[passDuration],[nopc],[freq],
[errorRadius],[semiMajor],[semiMinor],[orientation],[hdop]
,[speed],[course], [type]
,@ind,@user,'ARGOS_'+CAST([FK_ptt] as varchar(55))+'_'+replace(replace(' '+convert(varchar(10),date,112),'/',''),'/0','/')+replace(''+convert(varchar(5),date,108),':','')
FROM ecoreleve_sensor.dbo.T_argosgps WHERE PK_id in (
select data_PK_ID from data where r=1
) and checked = 0

-- check duplicate station before insert data in @data_without_duplicate
insert into  @data_duplicate  
select d.data_id, s.TSta_PK_ID
from @data_to_insert d join TStations s on d.lat=s.LAT and d.lon = s.LON and d.date_ = s.DATE and s.Name = d.name


-- insert data creating new station and linked Tsta_PK_ID to data_id using FieldWorker1
Insert into TStations (FieldActivity_ID,FieldActivity_Name,Name,DATE, LAT,LON,ELE,Creation_date, Creator,regionUpdate, FieldWorker1,Name_DistanceFromObs)
output inserted.TSta_PK_ID,inserted.FieldWorker1, inserted.Name_DistanceFromObs into @output
select 
27
,'Automatic data acquisition'
,'ARGOS_'+CAST(platform_ as varchar(55))+'_'+replace(replace(' '+convert(varchar(10),date_,112),'/',''),'/0','/')+replace(''+convert(varchar(5),date_,108),':','')
,date_
,lat
,lon
,ele
,getdate()
,creator
,0
,data_id
,type_
from @data_to_insert where data_id not in (select data_id from @data_duplicate)
SET @NbINserted=@@ROWCOUNT

-- insert in TProtocol_ArgosDataArgos data Argos From type = 'ARGOS'
Insert into TProtocol_ArgosDataArgos (FK_TSta_ID,FK_TInd_ID, TADA_LC, TADA_IQ , TADA_NbMsg, [TADA_NbMsg>-120Db], TADA_BestLevel , TADA_PassDuration , TADA_NOPC, TADA_Frequency)
SELECT o.sta_id, FK_ind, lc, iq, nbMsg,nbMsg120dB, bestLevel,passDuration,nopc,freq
FROM @data_to_insert i 
join @output o on o.data_id=i.data_id
where i.data_id not in (select data_id from @data_duplicate) and i.type_ = 'arg'

-- insert in TProtocol_ArgosDataArgos data Argos From type = 'GPS'
Insert into TProtocol_ArgosDataGPS (FK_TSta_ID,FK_TInd_ID,TADG_Course,TADG_Speed)
select o.sta_id, FK_ind,course,speed
FROM @data_to_insert i 
join @output o on o.data_id=i.data_id
where i.data_id not in (select data_id from @data_duplicate) and i.type_ = 'gps'


Insert into TArgosEngineeringData ( 
[TArE_PTT],[TArE_TXDATE],[TArE_PTTDATE]
,[TArE_SAT],[TArE_ACT_CNT],[TArE_TX_CNT]
,[TArE_TEMP],[TArE_BATT],[TArE_Fix_Time]
,[TArE_SAT_CNT],[TArE_Reset_Hours],[TArE_Fix_Days]
,[TArE_Season],[TArE_Shunt],[TarE_Nearest_FK_TSTA_ID], [creation_date]
)
SELECT
[FK_ptt],[txDate],[pttDate]
,[satId],[activity],[txCount]
,[temp],[batt],[fixTime]
,[satCount],[resetHours],[fixDays]
 ,[season],[shunt],s.TSta_PK_ID,GETDATE()
From ecoReleve_Sensor.dbo.Tgps_engineering e 
join TStations s on	e.latestLat = s.lat and e.latestLon = s.lon
where s.TSta_PK_ID in (select sta_id from @output) 

update TStations set FieldWorker1= null, Name_DistanceFromObs=null where TSta_PK_ID in (select sta_id from @output)
update ecoreleve_sensor.dbo.T_argosgps set imported = 1 where PK_id in (select data_id from @data_to_insert)
update V_dataARGOS_GPS_with_IndivEquip set checked = 1 where ptt = @ptt and ind_id = @ind

SET @nb_insert = @NbINserted
SELECT @exist = COUNT(*) FROM @data_duplicate
SET @error=@@ERROR

RETURN
END







GO



