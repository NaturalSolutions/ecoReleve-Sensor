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

    TStation = relationship(Station)


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

    TStation = relationship(Station)


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

    TStation = relationship(Station)


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

    TStation = relationship(Station)


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

    TStation = relationship(Station)


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

    TStation = relationship(Station)


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

    TStation = relationship(Station)


