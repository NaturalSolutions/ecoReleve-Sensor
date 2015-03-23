

/****** Object:  View [dbo].[V_dataRFID_as_file]    Script Date: 19/12/2014 15:20:08 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO






ALTER view [dbo].[V_dataRFID_as_file]
as 
with toto as 
(SELECT 
      rfid.[FK_obj] as id_obj    
	  ,obj.identifier as identifier
	  ,rfid.[FK_creator] as id_creator
      ,rfid.[checked] as checked
	, count (distinct chip_code) as nb_chip_code
	 , count (chip_code) as total_scan
	-- , rfid.frequency_hour as frequency_hour
	 , e.begin_date as begin_date
	 ,e.end_date as end_date
	 ,e.lat as lat
	 ,e.lon as lon
	 ,s.Name as site_name
	,s.name_Type as site_type
	,rfid.creation_date
	,Max(rfid.date_) as last_scan
	,Min(rfid.date_) as first_scan
	


  FROM [ecoReleve_DataNew].[dbo].[T_DataRfid] rfid
  join [dbo].[T_Object] obj on rfid.FK_obj=obj.PK_id
  join [dbo].[T_MonitoredSiteEquipment] e on rfid.FK_obj=e.FK_obj
 and rfid.date_ >= e.begin_date and (rfid.date_ <= e.end_date or e.end_date is null)
  join [dbo].[TMonitoredStations] s on s.TGeo_pk_id=e.FK_site

  group by rfid.FK_obj, rfid.[FK_creator] ,rfid.[checked],obj.identifier,rfid.creation_date,s.Name,s.name_Type, e.begin_date,e.end_date,e.lat,e.lon ,rfid.checked

)

select * from toto 

--union

--(SELECT 
     -- rfid.[FK_obj] as id_obj    
	  --,obj.identifier as identifier
	  --,rfid.[FK_creator] as id_creator
      --,rfid.[checked] as checked
	--, count (distinct chip_code) as nb_chip_code
	 --, count (chip_code) as total_scan
	 --,NULL as begin_date
	 --,NULL as end_date
	 --,NULL as lat
	 --,NULL as lon
	 --,NULL as site_name
	--,NULL as site_type
	--,rfid.creation_date
	--,Max(rfid.date_) as last_scan
	--,Min(rfid.date_) as first_scan
	


  --FROM [ecoReleve_DataNew].[dbo].[T_DataRfid] rfid
  --join [dbo].[T_Object] obj on rfid.FK_obj=obj.PK_id
  --where rfid.creation_date not in (select creation_date from toto)
  --group by rfid.FK_obj, rfid.[FK_creator] ,rfid.[checked],obj.identifier,rfid.creation_date,rfid.checked)




GO





