# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, Index, Integer, Numeric, String, Text, Unicode, text
from sqlalchemy.dialects.mssql.base import BIT
from sqlalchemy.orm import relationship
from ..models import Base, GenProtocole, Station, Individual, MonitoredSite



class TProtocolBirdBiometry(Base,GenProtocole):
    __tablename__ = 'TProtocol_Bird_Biometry'
    __table_args__ = (
        Index('Idx_Unique_Biometry_Individual_Station', 'FK_TInd_ID', 'FK_TSta_ID', unique=True),
    )

    PK = Column(Integer, primary_key=True)
    FK_TInd_ID = Column(Integer)
    FK_TSta_ID = Column(ForeignKey(Station.id))
    Id_Assistant = Column(Integer)
    Id_Observer = Column(Integer)
    Id_Sex = Column(Integer)
    Name_Sex = Column(Unicode(100))
    Id_Age = Column(Integer)
    Name_Age = Column(Unicode(100))
    Weight = Column(Float(53))
    Half_Culmen = Column(Float(53))
    Skull = Column(Float(53))
    Wings = Column(Float(53))
    Tarso_Metatarsus = Column(Float(53))
    Feather_Occipital = Column(Float(53))
    Feather_Black_Display = Column(Float(53))
    Feather_White_Display = Column(Float(53))
    Identification_criteria = Column(Unicode(500))
    Identification_type = Column(Unicode(10))
    Comments = Column(String(1000, 'French_CI_AS'))
    Adiposity_note = Column(Integer)
    Muscle_note = Column(Integer)
    Feather_thirdPrimaryFlight_length = Column(Integer)
    Sampled = Column(BIT, nullable=False, server_default=text("((0))"))
    Tail = Column(Float(53))
    Sternum = Column(Float(53))
    Feather_Black_White = Column(Float(53))
    Bill_length_feather = Column(Float(53))
    Bill_length_nostril = Column(Float(53))
    Bill_width = Column(Float(53))
    Toe_middle_length = Column(Float(53))
    Bird_collected = Column(BIT, nullable=False, server_default=text("((0))"))
    Toe_middle_width = Column(Float(53))
    Toe_middle_width_max = Column(Float(53))
    Toe_middle_width_min = Column(Float(53))

    TStation = relationship('Station')


class TProtocolBuildingAndActivity(Base,GenProtocole):
    __tablename__ = 'TProtocol_Building_and_Activities'
    __table_args__ = (
        Index('Unique_BuildingAndActivities_Impact_Station', 'FK_TSta_ID', 'Id_Impact', unique=True),
    )

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey(Station.id), nullable=False, index=True)
    Element_Nb = Column(Integer)
    Id_Impact = Column(Integer, index=True)
    Name_Impact = Column(Unicode(250))
    Comments = Column(Unicode(255))

    TStation = relationship('Station')


class TProtocolChiropteraCapture(Base,GenProtocole):
    __tablename__ = 'TProtocol_Chiroptera_capture'

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey(Station.id))
    Id_Taxon = Column(Integer, nullable=False)
    Name_Taxon = Column(String(1000, 'French_CI_AS'))
    Dead = Column(BIT, nullable=False, server_default=text("((0))"))
    Number = Column(Integer, server_default=text("((0))"))
    Hour = Column(DateTime)
    Ind_Id = Column(Unicode(50))
    Id_Age = Column(Integer, nullable=False)
    Name_Age = Column(String(200, 'French_CI_AS'))
    Id_Sex = Column(Integer)
    Name_Sex = Column(Unicode(255))
    Picture = Column(BIT, nullable=False, server_default=text("((0))"))
    Recatch = Column(BIT, nullable=False, server_default=text("((0))"))
    Recorded = Column(BIT, nullable=False, server_default=text("((0))"))
    Comments = Column(Unicode(255))
    FA = Column(Float(53))
    Tib = Column(Float(53))
    D3 = Column(Float(53))
    D3_1 = Column(Float(53))
    D3_2 = Column(Float(53))
    D3_3 = Column(Float(53))
    D4 = Column(Float(53))
    D4_1 = Column(Float(53))
    D4_2 = Column(Float(53))
    D5 = Column(Float(53))
    D5_1 = Column(Float(53))
    D5_2 = Column(Float(53))
    CM3 = Column(Float(53))
    D1 = Column(Float(53))
    Claw_D1 = Column(Float(53))
    tragus_Lenght = Column(Float(53))
    tragus_Width = Column(Float(53))
    Weight = Column(Float(53))
    CommentsBiometry = Column(Unicode(255))
    Id_Rep_Male = Column(Integer)
    Name_Rep_Male = Column(Unicode(255))
    Id_Rep_Female = Column(Integer)
    Name_Rep_Female = Column(Unicode(255))
    Id_Maturity_Female = Column(Integer)
    Name_Maturity_Female = Column(Unicode(255))
    CommentsPhysiology = Column(Unicode(255))
    Sampled = Column(BIT, nullable=False, server_default=text("((0))"))

    TStation = relationship('Station')


class TProtocolChiropteraDetection(Base,GenProtocole):
    __tablename__ = 'TProtocol_Chiroptera_detection'

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey(Station.id), index=True)
    Id_Taxon = Column(Integer, index=True)
    Name_Taxon = Column(String(1000, 'French_CI_AS'))
    Ind_Id = Column(Unicode(50), index=True)
    Number = Column(Integer, index=True)
    Time = Column(DateTime)
    Comments = Column(Unicode(255))
    File_name = Column(Unicode(255))
    Id_Call_type = Column(Integer)
    Name_Call_type = Column(Unicode(255))
    Flutter_0_min = Column(Float(53))
    Flutter_0_max = Column(Float(53))
    Id_Activity_type = Column(Integer)
    Name_Activity_type = Column(Unicode(255))
    Recorded = Column(BIT, nullable=False, server_default=text("((0))"))
    Id_Record_type = Column(Integer)
    Name_Record_type = Column(Unicode(50))

    TStation = relationship('Station')


class TProtocolSimplifiedHabitat(Base,GenProtocole):
    __tablename__ = 'TProtocol_Simplified_Habitat'

    PK = Column(Integer, primary_key=True, index=True)
    Name_Habitat = Column(Unicode(255))
    Id_Habitat = Column(Integer, index=True)
    Name_Habitat2 = Column(Unicode(255))
    Id_Habitat2 = Column(Integer)
    Id_Geomorphology = Column(Integer)
    Name_Geomorphology = Column(Unicode(255))
    Name_Flora_Main_Species_1 = Column(Unicode(255))
    Id_Flora_Main_Species_1 = Column(Integer, index=True)
    Name_Flora_Main_Species_2 = Column(Unicode(255))
    Id_Flora_Main_Species_2 = Column(Integer, index=True)
    Name_Flora_Main_Species_3 = Column(Unicode(255))
    Id_Flora_Main_Species_3 = Column(Integer, index=True)
    Vegetation_cover = Column(Integer)
    Perennial_cover = Column(Integer)
    Comments = Column(Unicode(255))
    FK_TSta_ID = Column(ForeignKey(Station.id), nullable=False, unique=True)
    Cultivated_1 = Column(BIT, nullable=False, server_default=text("((0))"))
    Cultivated_2 = Column(BIT, nullable=False, server_default=text("((0))"))
    Cultivated_3 = Column(BIT, nullable=False, server_default=text("((0))"))

    TStation = relationship('Station')


class TProtocolStationDescription(Base,GenProtocole):
    __tablename__ = 'TProtocol_Station_Description'

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey(Station.id))
    Id_Landscape = Column(Integer)
    Name_Landscape = Column(Unicode(500))
    Id_VegetationType = Column(Integer)
    Name_VegetationType = Column(Unicode(100))
    Name_Flora_Main_Species_1 = Column(Unicode)
    Name_Flora_Main_Species_2 = Column(Unicode)
    Name_Flora_Main_Species_3 = Column(Unicode)
    Id_Substrat = Column(Integer)
    Name_Substrat = Column(Unicode(250))
    Id_Topography = Column(Integer)
    Name_Topography = Column(Unicode(250))
    Id_Exposition = Column(Integer)
    Name_Exposition = Column(Unicode(250))
    Id_Slope_Class = Column(Integer)
    Name_Slope_Class = Column(Unicode(250))
    Area = Column(Float(53))
    Cover = Column(Float(53))
    Id_Moisture = Column(Integer)
    Name_Moisture = Column(Unicode(100))
    Id_Density_herbs = Column(Integer)
    Name_Density_herbs = Column(Unicode(100))
    Id_Density_bushes = Column(Integer)
    Name_Density_bushes = Column(Unicode(100))
    Id_Density_trees = Column(Integer)
    Name_Density_trees = Column(Unicode(100))
    Id_Greeness_herbs = Column(Integer)
    Name_Greeness_herbs = Column(Unicode(100))
    Id_Greeness_bushes = Column(Integer)
    Name_Greeness_bushes = Column(Unicode(100))
    Id_Greeness_trees = Column(Integer)
    Name_Greeness_trees = Column(Unicode(100))
    Phenology_Vegetative_herbs = Column(BIT, nullable=False, server_default=text("((0))"))
    Phenology_Flowering_herbs = Column(BIT, nullable=False, server_default=text("((0))"))
    Phenology_Seeding_herbs = Column(BIT, nullable=False, server_default=text("((0))"))
    Phenology_Vegetative_bushes = Column(BIT, nullable=False, server_default=text("((0))"))
    Phenology_Flowering_bushes = Column(BIT, nullable=False, server_default=text("((0))"))
    Phenology_Seeding_bushes = Column(BIT, nullable=False, server_default=text("((0))"))
    Phenology_Vegetative_trees = Column(BIT, nullable=False, server_default=text("((0))"))
    Phenology_Flowering_trees = Column(BIT, nullable=False, server_default=text("((0))"))
    Phenology_Seeding_trees = Column(BIT, nullable=False, server_default=text("((0))"))
    Last_Rain_event = Column(Unicode(100))
    Houbara_Suitable = Column(BIT, nullable=False, server_default=text("((0))"))
    Comments = Column(Text(collation='French_CI_AS'))

    TStation = relationship('Station')


class TProtocolVertebrateIndividualDeath(Base,GenProtocole):
    __tablename__ = 'TProtocol_Vertebrate_Individual_Death'
    __table_args__ = (
        Index('Ind_TProtoVDeath_FKSta_FKInd', 'FK_TSta_ID', 'FK_TInd_ID'),
    )

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey(Station.id), nullable=False, index=True)
    FK_TInd_ID = Column(Integer, index=True)
    Id_Remains = Column(Integer)
    Name_Remains = Column(Unicode(250))
    Id_Death_Time = Column(Integer)
    Name_Death_Time = Column(Unicode(250))
    Id_Death_Reason = Column(Integer)
    Name_Death_Reason = Column(Unicode(250))
    Identification_criteria = Column(Unicode(500))
    Sure_reason = Column(BIT, nullable=False, server_default=text("((0))"))
    Identification_type = Column(Unicode(10))
    Comments = Column(Unicode(500))
    Name_Taxon = Column(Unicode(255))
    Id_Taxon = Column(Integer, index=True)
    Sampled = Column(BIT, nullable=False, server_default=text("((0))"))

    TStation = relationship('Station')


class TProtocolCaptureGroup(Base,GenProtocole):
    __tablename__ = 'TProtocol_Capture_Group'
    __table_args__ = (
        Index('Ind_TProtoCaptureGroup_FKSta_IDSpecy', 'FK_TSta_ID', 'Id_Taxon', unique=True),
    )

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey('TStations.TSta_PK_ID'), nullable=False, index=True)
    Id_Capture_Method = Column(Integer)
    Name_Capture_Method = Column(Unicode(250))
    Nb_Operator = Column(Integer)
    Time_Begin = Column(DateTime)
    Failure_reason = Column(Unicode(255))
    Comments = Column(Unicode(255))
    Id_Taxon = Column(Integer, index=True)
    Name_Taxon = Column(Unicode(255))
    Time_End = Column(DateTime)
    Nb_Individuals = Column(Integer)

    TStation = relationship('Station')


class TProtocolCaptureIndividual(Base,GenProtocole):
    __tablename__ = 'TProtocol_Capture_Individual'
    __table_args__ = (
        Index('Unique_Individual_Capture_Station2', 'FK_TSta_ID', 'FK_TInd_ID', unique=True),
        Index('Unique_Individual_Capture_Station1', 'FK_Group', 'FK_TInd_ID', unique=True)
    )

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey('TStations.TSta_PK_ID'), nullable=False, index=True)
    FK_TInd_ID = Column(Integer, index=True)
    FK_Group = Column(ForeignKey('TProtocol_Capture_Group.PK'), index=True)
    Id_Assistant = Column(Integer)
    Id_Observer = Column(Integer)
    Release_Ind_Condition = Column(Unicode(255))
    Identification_criteria = Column(Unicode(500))
    Identification_type = Column(Unicode(10))
    Comments = Column(Unicode(255))
    Time_Capture = Column(DateTime)
    Time_Release = Column(DateTime)

    TProtocol_Capture_Group = relationship('TProtocolCaptureGroup')
    TStation = relationship('Station')


class TProtocolClutchDescription(Base,GenProtocole):
    __tablename__ = 'TProtocol_Clutch_Description'

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey('TStations.TSta_PK_ID'), nullable=False, index=True)
    FK_Nest = Column(ForeignKey('TProtocol_Nest_Description.PK'), index=True)
    Egg_code = Column(Unicode(50))
    Weight = Column(Numeric(9, 2))
    Length = Column(Numeric(9, 2))
    Width = Column(Numeric(9, 2))
    Name_EggStatus = Column(Unicode(250))
    Id_EggStatus = Column(Integer, index=True)
    Sampled = Column(BIT, nullable=False, server_default=text("((0))"))
    Collected = Column(BIT, nullable=False, server_default=text("((0))"))
    Comments = Column(Unicode(255))
    Measured_by = Column(Integer)

    TProtocol_Nest_Description = relationship('TProtocolNestDescription')
    TStation = relationship('Station')


class TProtocolEntomoPopulation(Base,GenProtocole):
    __tablename__ = 'TProtocol_Entomo_population'

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey('TStations.TSta_PK_ID'), nullable=False, index=True)
    Id_Capture = Column(Integer, index=True)
    Name_Capture = Column(Unicode(500))
    Comments = Column(Unicode(255))

    TStation = relationship('Station')


class TProtocolNestDescription(Base,GenProtocole):
    __tablename__ = 'TProtocol_Nest_Description'

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey('TStations.TSta_PK_ID'), nullable=False, index=True)
    Nb_Egg = Column(Integer)
    Picture = Column(BIT, nullable=False, server_default=text("((0))"))
    Comments = Column(Unicode(255))
    FK_TIND_ID = Column(Integer, index=True)
    Identification_type = Column(Unicode(10))
    Identification_criteria = Column(Unicode(500))
    ID_Clutch_Size = Column(Integer)
    Name_Clutch_Size = Column(Unicode(250))
    Id_Taxon = Column(Integer, nullable=False, index=True)
    Name_Taxon = Column(Unicode(255))
    Id_Clutch_Description = Column(Integer)
    Name_Clutch_Description = Column(Unicode(250))
    Dummy_egg = Column(BIT, nullable=False, server_default=text("((0))"))

    TStation = relationship('Station')


class TProtocolPhytosociologyHabitat(Base,GenProtocole):
    __tablename__ = 'TProtocol_Phytosociology_habitat'

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey('TStations.TSta_PK_ID'), nullable=False, index=True)
    Id_Milieu = Column(Integer, index=True)
    Name_Milieu = Column(Unicode(500))
    Id_Habitat2 = Column(Integer)
    Name_Habitat2 = Column(Unicode(500))
    Id_Exposition = Column(Integer, index=True)
    Name_Exposition = Column(Unicode(50))
    Id_Topography = Column(Integer, index=True)
    Name_Topography = Column(Unicode(250))
    Id_Slope_Class = Column(Integer, index=True)
    Name_Slope_Class = Column(Unicode(50))
    Area = Column(Float(53))
    Vegetation_cover = Column(Float(53), server_default=text("(NULL)"))
    Id_Hydrography = Column(Integer, index=True)
    Name_Hydrography = Column(Unicode(250))
    Id_Substrat = Column(Integer, index=True)
    Name_Substrat = Column(Unicode(250))
    Comments = Column(Unicode(255))
    Id_micro_habitat = Column(Integer)
    Name_micro_habitat = Column(Unicode(250))
    Id_PH_class = Column(Integer, server_default=text("(NULL)"))
    Name_PH_class = Column(Unicode(50), server_default=text("(NULL)"))
    Id_soil_texture = Column(Integer, server_default=text("(NULL)"))
    Name_soil_texture = Column(Unicode(550), server_default=text("(NULL)"))
    Id_vegetation_series = Column(Integer, server_default=text("(NULL)"))
    Name_vegetation_series = Column(Unicode(550), server_default=text("(NULL)"))
    stratum_MossLichen_cover = Column(Integer, server_default=text("(NULL)"))
    stratum_Herbaceous_cover = Column(Integer, server_default=text("(NULL)"))
    stratum_Shrubby_cover = Column(Integer, server_default=text("(NULL)"))
    stratum_Arboreal_cover = Column(Integer, server_default=text("(NULL)"))
    stratum_Arboreal_height_avg = Column(Float(53), server_default=text("(NULL)"))
    stratum_Shrubby_height_avg = Column(Float(53), server_default=text("(NULL)"))
    stratum_Herbaceous_height_avg = Column(Float(53), server_default=text("(NULL)"))
    stratum_MossLichen_height_avg = Column(Float(53), server_default=text("(NULL)"))
    Habitat_Picture = Column(BIT, nullable=False, server_default=text("((0))"))
    VegSeries_Sure = Column(BIT, nullable=False, server_default=text("((0))"))

    TStation = relationship('Station')


class TProtocolPhytosociologyReleve(Base,GenProtocole):
    __tablename__ = 'TProtocol_Phytosociology_releve'
    __table_args__ = (
        Index('Unique_PhytosociologyCensus_Taxon_Station', 'Id_Taxon', 'FK_TSta_ID', unique=True),
    )

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey('TStations.TSta_PK_ID'), nullable=False, index=True)
    Id_Taxon = Column(Integer, nullable=False, index=True)
    Name_Taxon = Column(Unicode, nullable=False)
    Identity_sure = Column(BIT, nullable=False, server_default=text("((0))"))
    Sampled = Column(BIT, nullable=False, server_default=text("((0))"))
    Picture = Column(BIT, nullable=False, server_default=text("((0))"))
    Id_Global_Abondance_Dom = Column(Integer, index=True)
    Name_Global_Abondance_Dom = Column(Unicode(50))
    Id_Global_Sociability = Column(Integer, index=True)
    Name_Global_Sociability = Column(Unicode(25))
    Id_Phenology_BBCH1 = Column(Integer, index=True)
    Name_Phenology_BBCH1 = Column(Unicode(25))
    Id_Phenology_BBCH2 = Column(Integer, index=True)
    Name_Phenology_BBCH2 = Column(Unicode(25))
    Id_Nb_Individuals = Column(Integer, index=True)
    Name_Nb_Individuals = Column(Unicode(250))
    Validator = Column(Integer)
    Comments = Column(Unicode(255))
    Cultivated = Column(BIT, nullable=False, server_default=text("((0))"))

    TStation = relationship('Station')


class TProtocolReleaseGroup(Base,GenProtocole):
    __tablename__ = 'TProtocol_Release_Group'
    __table_args__ = (
        Index('Ind_TProtoReleaseGroup_FKSta_IDSpecy', 'FK_TSta_ID', 'Id_Taxon', unique=True),
    )

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey('TStations.TSta_PK_ID'), nullable=False, index=True)
    Id_Taxon = Column(Integer)
    Name_Taxon = Column(Unicode(255))
    Id_Release_Method = Column(Integer)
    Name_Release_Method = Column(Unicode(250))
    Comments = Column(Unicode(255))

    TStation = relationship('Station')


class TProtocolReleaseIndividual(Base,GenProtocole):
    __tablename__ = 'TProtocol_Release_Individual'
    __table_args__ = (
        Index('Unique_Individual_Release_Station', 'FK_TInd_ID', 'FK_Group', 'FK_TSta_ID', unique=True),
    )

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey('TStations.TSta_PK_ID'), nullable=False, index=True)
    FK_TInd_ID = Column(Integer, index=True)
    FK_Group = Column(ForeignKey('TProtocol_Release_Group.PK'), index=True)
    Comments = Column(Unicode(255))

    TProtocol_Release_Group = relationship('TProtocolReleaseGroup')
    TStation = relationship('Station')


class TProtocolSightingCondition(Base,GenProtocole):
    __tablename__ = 'TProtocol_Sighting_conditions'

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey('TStations.TSta_PK_ID'), nullable=False, unique=True)
    Obs_duration_old = Column(Integer)
    Id_Weather = Column(Integer, index=True)
    Name_Weather = Column(Unicode(250))
    Id_Wind_Force = Column(Integer, index=True)
    Name_Wind_Force = Column(Unicode(250))
    Temperature = Column(Integer)
    Comments = Column(Unicode(255))
    Start_time = Column(DateTime)
    End_time = Column(DateTime)
    Observation_Duration = Column(DateTime)
    Visibility = Column(BIT, nullable=False, server_default=text("((0))"))
    Observation_Incomplete = Column(BIT, nullable=False, server_default=text("((0))"))
    Id_Observation_Tool = Column(Integer)
    Name_Observation_Tool = Column(Unicode(250))

    TStation = relationship('Station')


class TProtocolStationEquipment(Base,GenProtocole):
    __tablename__ = 'TProtocol_Station_equipment'

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey('TStations.TSta_PK_ID'), nullable=False)
    id_action_type = Column(Integer, nullable=False)
    name_action_type = Column(Unicode(250), nullable=False)
    id_sensor_type = Column(Integer)
    name_sensor_type = Column(Unicode(250), nullable=False)
    Comments = Column(Unicode(255))

    TStation = relationship('Station')


class TProtocolTrackClue(Base,GenProtocole):
    __tablename__ = 'TProtocol_Track_clue'
    __table_args__ = (
        Index('Unique_TrackClue_Taxon_Track_Station', 'id_taxon', 'Id_Track_clue', 'FK_TSta_ID', unique=True),
    )

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey('TStations.TSta_PK_ID'), nullable=False, index=True)
    Id_Track_clue = Column(Integer, index=True)
    Name_Track_clue = Column(Unicode(250))
    Comments = Column(Unicode(255))
    id_taxon = Column(Integer)
    name_taxon = Column(Unicode(250))
    Identity_sure = Column(BIT, nullable=False, server_default=text("((1))"))
    Number_Track_clue = Column(Integer)
    Sampled = Column(BIT, nullable=False, server_default=text("((0))"))

    TStation = relationship('Station')


class TProtocolTransect(Base,GenProtocole):
    __tablename__ = 'TProtocol_Transects'

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey('TStations.TSta_PK_ID'), nullable=False, index=True)
    Num_Bound = Column(Integer, index=True, server_default=text("((0))"))
    Num_Transect = Column(Integer, index=True, server_default=text("((0))"))
    Comments = Column(Unicode(255))
    Id_Observer = Column(Integer)
    Id_Assistant = Column(Integer)

    TStation = relationship('Station')


class TProtocolVertebrateGroup(Base,GenProtocole):
    __tablename__ = 'TProtocol_Vertebrate_Group'
    __table_args__ = (
        Index('Unique_VertebrateGroup_Taxon_Station_DistBearing', 'FK_TSta_ID', 'Id_Taxon', 'Measured_Distance', 'Estimated_Distance', 'AngleNorth', 'AngleTrack', unique=True),
    )

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey('TStations.TSta_PK_ID'), nullable=False, index=True)
    Name_Taxon = Column(Unicode(250))
    Id_Taxon = Column(Integer, nullable=False, index=True)
    Identity_sure = Column(BIT, nullable=False, server_default=text("((0))"))
    Ident_Occasional = Column(BIT, nullable=False, server_default=text("((0))"))
    Nb_Adult_Male = Column(Integer, server_default=text("((0))"))
    Nb_Adult_Female = Column(Integer, server_default=text("((0))"))
    Nb_Adult_Indeterminate = Column(Integer, server_default=text("((0))"))
    Nb_Juvenile_Male = Column(Integer, server_default=text("((0))"))
    Nb_Juvenile_Female = Column(Integer, server_default=text("((0))"))
    Nb_Juvenile_Indeterminate = Column(Integer, server_default=text("((0))"))
    Nb_NewBorn_Male = Column(Integer, server_default=text("((0))"))
    Nb_NewBorn_Female = Column(Integer, server_default=text("((0))"))
    Nb_NewBorn_Indeterminate = Column(Integer, server_default=text("((0))"))
    Nb_Indeterminate = Column(Integer, server_default=text("((0))"))
    Name_Behaviour = Column(Unicode(250))
    Id_Behaviour = Column(Integer, index=True)
    Disturbed = Column(BIT, nullable=False, server_default=text("((0))"))
    Comments = Column(Unicode(300))
    Measured_Distance = Column(Numeric(9, 2))
    AngleNorth = Column(Numeric(9, 2))
    Estimated_Distance = Column(Numeric(9, 2))
    AngleTrack = Column(Numeric(9, 2))
    # Nb_Total = Column(Integer)
    # timestamp = Column(DateTime, nullable=False)
    observation_time = Column(DateTime, server_default=text("(NULL)"))

    TStation = relationship('Station')

    def __init__(self):
        self.Id_Taxon=10


class TProtocolVertebrateIndividual(Base,GenProtocole):
    __tablename__ = 'TProtocol_Vertebrate_Individual'

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey('TStations.TSta_PK_ID'), nullable=False, index=True)
    Fk_TInd_ID = Column(Integer, index=True)
    Fk_Group = Column(Integer, index=True)
    frequency = Column(Integer)
    id_sex = Column(Integer, index=True)
    name_sex = Column(Unicode(50), index=True)
    id_age = Column(Integer, index=True)
    name_age = Column(Unicode(50), index=True)
    Id_signal_type = Column(Integer)
    Name_signal_type = Column(Unicode(250))
    Id_Posture = Column(Integer)
    Name_Posture = Column(Unicode(250))
    Id_Behaviour = Column(Integer, index=True)
    Name_Behaviour = Column(Unicode(250), index=True)
    Identification_type = Column(String(10, 'French_CI_AS'))
    Identification_criteria = Column(Unicode(500))
    Comments = Column(Unicode(540))
    Sampled = Column(BIT, server_default=text("((0))"))
    Disturbed = Column(BIT)
    timestamp = Column(DateTime, nullable=False)

    TStation = relationship('Station')