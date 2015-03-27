-- =============================================
-- Author:    Romain FABBRO
-- Create date: 2015-03-27
-- Description: View to retrieve Last Imported station from 3 days and without protocols
-- =============================================



Create View V_lastStation_3Days_without_Protocols 
  as
  (select * from [dbo].[TStations] where Creation_date > DATEADD (day , -3 , GETDATE() ) )
  except  
  (select s.* from [dbo].[TStations] s
  join TProtocol_Bird_Biometry b  on s.TSta_PK_ID = b.FK_TSta_ID
  join TProtocol_Building_and_Activities bd  on s.TSta_PK_ID = bd.FK_TSta_ID
  join TProtocol_Capture_Group cg  on s.TSta_PK_ID = cg.FK_TSta_ID
  join TProtocol_Capture_Individual ci  on s.TSta_PK_ID = ci.FK_TSta_ID
  join TProtocol_Chiroptera_capture cc  on s.TSta_PK_ID = cc.FK_TSta_ID
  join TProtocol_Chiroptera_detection cd  on s.TSta_PK_ID = cd.FK_TSta_ID
  join TProtocol_Clutch_Description cl on s.TSta_PK_ID = cl.FK_TSta_ID
  join TProtocol_Habitat_stratified hs on s.TSta_PK_ID = hs.FK_TSta_ID
  join TProtocol_Nest_Description nd on s.TSta_PK_ID = nd.FK_TSta_ID
  join TProtocol_Phytosociology_habitat ph on s.TSta_PK_ID = ph.FK_TSta_ID
  join TProtocol_Phytosociology_releve pr on s.TSta_PK_ID = pr.FK_TSta_ID
  join TProtocol_Release_Group rg on s.TSta_PK_ID = rg.FK_TSta_ID
  join TProtocol_Release_Individual ri on s.TSta_PK_ID = ri.FK_TSta_ID
  join TProtocol_Sampling sa on s.TSta_PK_ID = sa.FK_TSta_ID
  join TProtocol_Sighting_conditions sc on s.TSta_PK_ID = sc.FK_TSta_ID
  join TProtocol_Simplified_Habitat sh on s.TSta_PK_ID = sh.FK_TSta_ID
  join TProtocol_Station_Description sd on s.TSta_PK_ID = sd.FK_TSta_ID
  join TProtocol_Station_equipment se on s.TSta_PK_ID = se.FK_TSta_ID
  join TProtocol_Track_clue tc on s.TSta_PK_ID = tc.FK_TSta_ID
  join TProtocol_Transects tr on s.TSta_PK_ID = tr.FK_TSta_ID
  join TProtocol_Vertebrate_Group vg on s.TSta_PK_ID = vg.FK_TSta_ID
  join TProtocol_Vertebrate_Individual vi on s.TSta_PK_ID = vi.FK_TSta_ID
  join TProtocol_Vertebrate_Individual_Death vid on s.TSta_PK_ID = vid.FK_TSta_ID
  join TProtocol_Vertebrate_interview vint on s.TSta_PK_ID = vint.FK_TSta_ID
  where s.Creation_date > DATEADD (day , -3 , GETDATE()) ) 