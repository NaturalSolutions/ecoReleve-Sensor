# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, Float, ForeignKey, Index, Integer, Numeric, SmallInteger, String, Table, Text, Unicode, UnicodeText, VARBINARY, text
from sqlalchemy.dialects.mssql.base import BIT
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


t_SYS_Disk_usage_by_Table = Table(
    'SYS_Disk_usage_by_Table', metadata,
    Column('Table_name', Unicode(128)),
    Column('Nb_records', BigInteger),
    Column('Total_kB', BigInteger),
    Column('Data_kB', BigInteger),
    Column('Index_kB', BigInteger),
    Column('Unused_kB', BigInteger)
)


t_TMapSelectionManager = Table(
    'TMapSelectionManager', metadata,
    Column('TSMan_ID', Integer, nullable=False),
    Column('TSMan_sp_name', Unicode),
    Column('TSMan_Layer_Name', Unicode(500)),
    Column('TSMan_Description', Unicode(500)),
    Column('TSMan_FK_Theme', Integer),
    Column('TSMan_AdminQry', BIT, nullable=False)
)


class TMonitoredStation(Base):
    __tablename__ = 'TMonitoredStations'
    __table_args__ = (
        Index('idx_Tmonitoredstations', 'name_Type', 'Name'),
        Index('idx_Tmonitoredstations_name', 'Name', 'TGeo_pk_id', 'Creation_date', 'Creator', 'Active', 'id_Type', 'name_Type'),
        Index('NonClusteredIndex-20140904-095516', 'name_Type', 'Name', 'TGeo_pk_id', 'Creation_date', 'Creator', 'Active', 'id_Type', unique=True)
    )

    TGeo_pk_id = Column(Integer, primary_key=True)
    Name = Column(Unicode(50))
    Creation_date = Column(DateTime)
    Creator = Column(Integer)
    Active = Column(BIT, nullable=False)
    id_Type = Column(Integer)
    name_Type = Column(Unicode(200))


t_TMonitoredStations_Positions = Table(
    'TMonitoredStations_Positions', metadata,
    Column('TGeoPos_PK_ID', Integer, nullable=False),
    Column('TGeoPos_FK_TGeo_ID', ForeignKey('TMonitoredStations.TGeo_pk_id'), nullable=False),
    Column('TGeoPos_LAT', Numeric(9, 5)),
    Column('TGeoPos_LON', Numeric(9, 5)),
    Column('TGeoPos_ELE', Float(53)),
    Column('TGeoPos_Date', DateTime),
    Column('TGeoPos_Begin_Date', DateTime),
    Column('TGeoPos_End_Date', DateTime),
    Column('TGeoPos_Comments', Unicode),
    Column('TGeoPos_Precision', Integer),
    Column('FK_creator', Integer),
    Index('idx_Tmonitoredsiteposition_site', 'TGeoPos_FK_TGeo_ID', 'TGeoPos_Begin_Date')
)


t_TObj_Carac_theme = Table(
    'TObj_Carac_theme', metadata,
    Column('Carac_theme_Pk', Integer, nullable=False),
    Column('Fk_Object', Integer),
    Column('name', Unicode(250), nullable=False)
)


t_TObj_Carac_type = Table(
    'TObj_Carac_type', metadata,
    Column('Carac_type_Pk', Integer, nullable=False),
    Column('Fk_Theme', Integer),
    Column('label', Unicode(250), nullable=False),
    Column('name', Unicode(250), nullable=False),
    Column('Constant', BIT, nullable=False)
)


t_TObj_Carac_value = Table(
    'TObj_Carac_value', metadata,
    Column('Carac_value_Pk', Integer, nullable=False),
    Column('Fk_carac', Integer),
    Column('fk_object', Integer, nullable=False),
    Column('value', Unicode(250), nullable=False),
    Column('value_precision', Unicode(1000)),
    Column('begin_date', DateTime, nullable=False),
    Column('end_date', DateTime),
    Column('creation_date', DateTime, nullable=False),
    Column('comments', Unicode(255)),
    Column('object_type', Unicode(20)),
    Column('uniquePTT', Unicode(271)),
    Column('uniqueReleaseCode', Unicode(253)),
    Column('uniqueRadioSN', Unicode(271)),
    Column('uniqueChipCode', Unicode(253)),
    Column('timestamp', DateTime, nullable=False),
    Index('idx_TObjCaracValue_FKobjectFKcaracBeginDate_With_ValueValuePrecisionEndDate', 'fk_object', 'Fk_carac', 'begin_date', 'value', 'value_precision', 'end_date')
)


t_TObj_Obj_CaracList = Table(
    'TObj_Obj_CaracList', metadata,
    Column('Obj_CaracList_Pk', Integer, nullable=False),
    Column('fk_Object_type', Integer, nullable=False),
    Column('fk_Carac_type', Integer, nullable=False),
    Column('value_type', Unicode(250), nullable=False),
    Column('value_precision', Unicode(250)),
    Column('Constant', BIT, nullable=False),
    Column('available', BIT, nullable=False)
)


t_TObj_Obj_Type = Table(
    'TObj_Obj_Type', metadata,
    Column('Obj_Type_Pk', Integer, nullable=False),
    Column('name', Unicode(250), nullable=False),
    Column('relation', Unicode(250), nullable=False),
    Column('fath_obj', Integer),
    Column('fath_relation', Unicode(250)),
    Column('cardinality', Unicode(250))
)


t_TObj_Objects = Table(
    'TObj_Objects', metadata,
    Column('Object_Pk', Integer, nullable=False),
    Column('Id_object_type', Integer, nullable=False),
    Column('Name_object_type', Unicode(50), nullable=False),
    Column('Creation_date', DateTime),
    Column('original_id', Integer)
)


t_TProjection = Table(
    'TProjection', metadata,
    Column('TPj_SysCoord_Name', Unicode(50), nullable=False),
    Column('TPj_Parameters', Unicode, nullable=False),
    Column('TPj_Code_EPSG', Integer)
)


t_TProt_TTheEt = Table(
    'TProt_TTheEt', metadata,
    Column('TProt_PK_ID', Integer, nullable=False),
    Column('TTheEt_PK_ID', Integer, nullable=False)
)


class TProtocolArgosDataArgo(Base):
    __tablename__ = 'TProtocol_ArgosDataArgos'

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(ForeignKey('TStations.TSta_PK_ID'), nullable=False)
    FK_TInd_ID = Column(Integer, nullable=False)
    TADA_LC = Column(Unicode(2))
    TADA_IQ = Column(Integer)
    TADA_NbMsg = Column(Integer)
    TADA_NbMsg__120Db = Column('TADA_NbMsg>-120Db', Integer)
    TADA_BestLevel = Column(Integer)
    TADA_PassDuration = Column(Integer)
    TADA_NOPC = Column(Integer)
    TADA_Frequency = Column(Numeric(10, 1))
    TADA_Comments = Column(Unicode(250))
    lat = Column(Numeric(9, 5))
    lon = Column(Numeric(9, 5))
    date = Column(DateTime)

    TStation = relationship('TStation')


class TProtocolArgosDataGP(Base):
    __tablename__ = 'TProtocol_ArgosDataGPS'
    __table_args__ = (
        Index('NonClusteredIndex-20140903-094211', 'FK_TInd_ID', 'date', 'lat', 'lon'),
    )

    PK = Column(Integer, primary_key=True)
    FK_TSta_ID = Column(Integer, nullable=False)
    FK_TInd_ID = Column(Integer, nullable=False)
    TADG_Course = Column(Integer)
    TADG_Speed = Column(Integer)
    TADG_Comments = Column(Unicode(250))
    lat = Column(Numeric(9, 5))
    lon = Column(Numeric(9, 5))
    date = Column(DateTime)


t_TProtocol_Bird_Biometry = Table(
    'TProtocol_Bird_Biometry', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TInd_ID', Integer),
    Column('FK_TSta_ID', Integer),
    Column('Id_Assistant', Integer),
    Column('Id_Observer', Integer),
    Column('Id_Sex', Integer),
    Column('Name_Sex', Unicode(100)),
    Column('Id_Age', Integer),
    Column('Name_Age', Unicode(100)),
    Column('Weight', Float(53)),
    Column('Half_Culmen', Float(53)),
    Column('Skull', Float(53)),
    Column('Wings', Float(53)),
    Column('Tarso_Metatarsus', Float(53)),
    Column('Feather_Occipital', Float(53)),
    Column('Feather_Black_Display', Float(53)),
    Column('Feather_White_Display', Float(53)),
    Column('Identification_criteria', Unicode(500)),
    Column('Identification_type', Unicode(10)),
    Column('Comments', String(1000, 'French_CI_AS')),
    Column('Adiposity_note', Integer),
    Column('Muscle_note', Integer),
    Column('Feather_thirdPrimaryFlight_length', Integer),
    Column('Sampled', BIT, nullable=False),
    Column('Tail', Float(53)),
    Column('Sternum', Float(53)),
    Column('Feather_Black_White', Float(53)),
    Column('Bill_length_feather', Float(53)),
    Column('Bill_length_nostril', Float(53)),
    Column('Bill_width', Float(53)),
    Column('Toe_middle_length', Float(53)),
    Column('Bird_collected', BIT, nullable=False),
    Column('Toe_middle_width', Float(53)),
    Column('Toe_middle_width_max', Float(53)),
    Column('Toe_middle_width_min', Float(53))
)


t_TProtocol_Building_and_Activities = Table(
    'TProtocol_Building_and_Activities', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('Element_Nb', Integer),
    Column('Id_Impact', Integer),
    Column('Name_Impact', Unicode(250)),
    Column('Comments', Unicode(255))
)


t_TProtocol_Capture_Group = Table(
    'TProtocol_Capture_Group', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('Id_Capture_Method', Integer),
    Column('Name_Capture_Method', Unicode(250)),
    Column('Nb_Operator', Integer),
    Column('Time_Begin', DateTime),
    Column('Failure_reason', Unicode(255)),
    Column('Comments', Unicode(255)),
    Column('Id_Taxon', Integer),
    Column('Name_Taxon', Unicode(255)),
    Column('Time_End', DateTime),
    Column('Nb_Individuals', Integer)
)


t_TProtocol_Capture_Individual = Table(
    'TProtocol_Capture_Individual', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('FK_TInd_ID', Integer),
    Column('FK_Group', Integer),
    Column('Id_Assistant', Integer),
    Column('Id_Observer', Integer),
    Column('Release_Ind_Condition', Unicode(255)),
    Column('Identification_criteria', Unicode(500)),
    Column('Identification_type', Unicode(10)),
    Column('Comments', Unicode(255)),
    Column('Time_Capture', DateTime),
    Column('Time_Release', DateTime)
)


t_TProtocol_Chiroptera_capture = Table(
    'TProtocol_Chiroptera_capture', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer),
    Column('Id_Taxon', Integer, nullable=False),
    Column('Name_Taxon', String(1000, 'French_CI_AS')),
    Column('Dead', BIT, nullable=False),
    Column('Number', Integer),
    Column('Hour', DateTime),
    Column('Ind_Id', Unicode(50)),
    Column('Id_Age', Integer, nullable=False),
    Column('Name_Age', String(200, 'French_CI_AS')),
    Column('Id_Sex', Integer),
    Column('Name_Sex', Unicode(255)),
    Column('Picture', BIT, nullable=False),
    Column('Recatch', BIT, nullable=False),
    Column('Recorded', BIT, nullable=False),
    Column('Comments', Unicode(255)),
    Column('FA', Float(53)),
    Column('Tib', Float(53)),
    Column('D3', Float(53)),
    Column('D3_1', Float(53)),
    Column('D3_2', Float(53)),
    Column('D3_3', Float(53)),
    Column('D4', Float(53)),
    Column('D4_1', Float(53)),
    Column('D4_2', Float(53)),
    Column('D5', Float(53)),
    Column('D5_1', Float(53)),
    Column('D5_2', Float(53)),
    Column('CM3', Float(53)),
    Column('D1', Float(53)),
    Column('Claw_D1', Float(53)),
    Column('tragus_Lenght', Float(53)),
    Column('tragus_Width', Float(53)),
    Column('Weight', Float(53)),
    Column('CommentsBiometry', Unicode(255)),
    Column('Id_Rep_Male', Integer),
    Column('Name_Rep_Male', Unicode(255)),
    Column('Id_Rep_Female', Integer),
    Column('Name_Rep_Female', Unicode(255)),
    Column('Id_Maturity_Female', Integer),
    Column('Name_Maturity_Female', Unicode(255)),
    Column('CommentsPhysiology', Unicode(255)),
    Column('Sampled', BIT, nullable=False)
)


t_TProtocol_Chiroptera_detection = Table(
    'TProtocol_Chiroptera_detection', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer),
    Column('Id_Taxon', Integer),
    Column('Name_Taxon', String(1000, 'French_CI_AS')),
    Column('Ind_Id', Unicode(50)),
    Column('Number', Integer),
    Column('Time', DateTime),
    Column('Comments', Unicode(255)),
    Column('File_name', Unicode(255)),
    Column('Id_Call_type', Integer),
    Column('Name_Call_type', Unicode(255)),
    Column('Flutter_0_min', Float(53)),
    Column('Flutter_0_max', Float(53)),
    Column('Id_Activity_type', Integer),
    Column('Name_Activity_type', Unicode(255)),
    Column('Recorded', BIT, nullable=False),
    Column('Id_Record_type', Integer),
    Column('Name_Record_type', Unicode(50))
)


t_TProtocol_Clutch_Description = Table(
    'TProtocol_Clutch_Description', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('FK_Nest', Integer),
    Column('Egg_code', Unicode(50)),
    Column('Weight', Numeric(9, 2)),
    Column('Length', Numeric(9, 2)),
    Column('Width', Numeric(9, 2)),
    Column('Name_EggStatus', Unicode(250)),
    Column('Id_EggStatus', Integer),
    Column('Sampled', BIT, nullable=False),
    Column('Collected', BIT, nullable=False),
    Column('Comments', Unicode(255)),
    Column('Measured_by', Integer)
)


t_TProtocol_Entomo_population = Table(
    'TProtocol_Entomo_population', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('Id_Capture', Integer),
    Column('Name_Capture', Unicode(500)),
    Column('Comments', Unicode(255))
)


t_TProtocol_Habitat_stratified = Table(
    'TProtocol_Habitat_stratified', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer),
    Column('arbo', Float(53)),
    Column('subarbo', Float(53)),
    Column('arbu_very_high', Float(53)),
    Column('arbu_high', Float(53)),
    Column('arbu_medium_2', Float(53)),
    Column('arbu_medium_1', Float(53)),
    Column('arbu_low_2', Float(53)),
    Column('arbu_low_1', Float(53)),
    Column('herb_very_high', Float(53)),
    Column('herb_high', Float(53)),
    Column('herb_medium_2', Float(53)),
    Column('herb_medium_1', Float(53)),
    Column('herb_low_2', Float(53)),
    Column('herb_low_1', Float(53)),
    Column('herb_very_low', Float(53)),
    Column('bryo', Float(53)),
    Column('Id_Global_Veg_State', Integer),
    Column('Name_Global_Veg_State', UnicodeText(1073741823)),
    Column('Id_Phenology', Integer),
    Column('Name_Phenology', UnicodeText(1073741823)),
    Column('Id_Grazing', Integer),
    Column('Name_Grazing', UnicodeText(1073741823)),
    Column('Stalling', BIT, nullable=False),
    Column('Area', Float(53)),
    Column('Comments', Unicode(255))
)


class TProtocolIndividualEquipment(Base):
    __tablename__ = 'TProtocol_Individual_Equipment'

    PK_ID = Column(Integer, primary_key=True)
    FK_SAT_ID = Column(Integer)
    FK_IND_ID = Column(Integer)
    begin_date = Column(DateTime)
    end_date = Column(DateTime)


t_TProtocol_Nest_Description = Table(
    'TProtocol_Nest_Description', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('Nb_Egg', SmallInteger),
    Column('Picture', BIT, nullable=False),
    Column('Comments', Unicode(255)),
    Column('FK_TIND_ID', Integer),
    Column('Identification_type', Unicode(10)),
    Column('Identification_criteria', Unicode(500)),
    Column('ID_Clutch_Size', Integer),
    Column('Name_Clutch_Size', Unicode(250)),
    Column('Id_Taxon', Integer, nullable=False),
    Column('Name_Taxon', Unicode(255)),
    Column('Id_Clutch_Description', Integer),
    Column('Name_Clutch_Description', Unicode(250)),
    Column('Dummy_egg', BIT, nullable=False)
)


t_TProtocol_Phytosociology_habitat = Table(
    'TProtocol_Phytosociology_habitat', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('Id_Milieu', Integer),
    Column('Name_Milieu', Unicode(500)),
    Column('Id_Habitat2', Integer),
    Column('Name_Habitat2', Unicode(500)),
    Column('Id_Exposition', Integer),
    Column('Name_Exposition', Unicode(50)),
    Column('Id_Topography', Integer),
    Column('Name_Topography', Unicode(250)),
    Column('Id_Slope_Class', Integer),
    Column('Name_Slope_Class', Unicode(50)),
    Column('Area', Float(53)),
    Column('Vegetation_cover', Float(53)),
    Column('Id_Hydrography', Integer),
    Column('Name_Hydrography', Unicode(250)),
    Column('Id_Substrat', Integer),
    Column('Name_Substrat', Unicode(250)),
    Column('Comments', Unicode(255)),
    Column('Id_micro_habitat', Integer),
    Column('Name_micro_habitat', Unicode(250)),
    Column('Id_PH_class', Integer),
    Column('Name_PH_class', Unicode(50)),
    Column('Id_soil_texture', Integer),
    Column('Name_soil_texture', Unicode(550)),
    Column('Id_vegetation_series', Integer),
    Column('Name_vegetation_series', Unicode(550)),
    Column('stratum_MossLichen_cover', Integer),
    Column('stratum_Herbaceous_cover', Integer),
    Column('stratum_Shrubby_cover', Integer),
    Column('stratum_Arboreal_cover', Integer),
    Column('stratum_Arboreal_height_avg', Float(53)),
    Column('stratum_Shrubby_height_avg', Float(53)),
    Column('stratum_Herbaceous_height_avg', Float(53)),
    Column('stratum_MossLichen_height_avg', Float(53)),
    Column('Habitat_Picture', BIT, nullable=False),
    Column('VegSeries_Sure', BIT, nullable=False)
)


t_TProtocol_Phytosociology_releve = Table(
    'TProtocol_Phytosociology_releve', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('Id_Taxon', Integer, nullable=False),
    Column('Name_Taxon', Unicode, nullable=False),
    Column('Identity_sure', BIT, nullable=False),
    Column('Sampled', BIT, nullable=False),
    Column('Picture', BIT, nullable=False),
    Column('Id_Global_Abondance_Dom', Integer),
    Column('Name_Global_Abondance_Dom', Unicode(50)),
    Column('Id_Global_Sociability', Integer),
    Column('Name_Global_Sociability', Unicode(25)),
    Column('Id_Phenology_BBCH1', Integer),
    Column('Name_Phenology_BBCH1', Unicode(25)),
    Column('Id_Phenology_BBCH2', Integer),
    Column('Name_Phenology_BBCH2', Unicode(25)),
    Column('Id_Nb_Individuals', Integer),
    Column('Name_Nb_Individuals', Unicode(250)),
    Column('Validator', Integer),
    Column('Comments', Unicode(255)),
    Column('Cultivated', BIT, nullable=False)
)


t_TProtocol_Release_Group = Table(
    'TProtocol_Release_Group', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('Id_Taxon', Integer),
    Column('Name_Taxon', Unicode(255)),
    Column('Id_Release_Method', Integer),
    Column('Name_Release_Method', Unicode(250)),
    Column('Comments', Unicode(255))
)


t_TProtocol_Release_Individual = Table(
    'TProtocol_Release_Individual', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('FK_TInd_ID', Integer),
    Column('FK_Group', Integer),
    Column('Comments', Unicode(255))
)


t_TProtocol_Sampling = Table(
    'TProtocol_Sampling', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('Id_Sample', Integer),
    Column('Name_Sample', Unicode(500), nullable=False),
    Column('Comments', Unicode(255))
)


t_TProtocol_Sighting_conditions = Table(
    'TProtocol_Sighting_conditions', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('Obs_duration_old', Integer),
    Column('Id_Weather', Integer),
    Column('Name_Weather', Unicode(250)),
    Column('Id_Wind_Force', Integer),
    Column('Name_Wind_Force', Unicode(250)),
    Column('Temperature', Integer),
    Column('Comments', Unicode(255)),
    Column('Start_time', DateTime),
    Column('End_time', DateTime),
    Column('Observation_Duration', DateTime),
    Column('Visibility', BIT, nullable=False),
    Column('Observation_Incomplete', BIT, nullable=False),
    Column('Id_Observation_Tool', Integer),
    Column('Name_Observation_Tool', Unicode(250))
)


t_TProtocol_Simplified_Habitat = Table(
    'TProtocol_Simplified_Habitat', metadata,
    Column('PK', Integer, nullable=False),
    Column('Name_Habitat', Unicode(255)),
    Column('Id_Habitat', Integer),
    Column('Name_Habitat2', Unicode(255)),
    Column('Id_Habitat2', Integer),
    Column('Id_Geomorphology', Integer),
    Column('Name_Geomorphology', Unicode(255)),
    Column('Name_Flora_Main_Species_1', Unicode(255)),
    Column('Id_Flora_Main_Species_1', Integer),
    Column('Name_Flora_Main_Species_2', Unicode(255)),
    Column('Id_Flora_Main_Species_2', Integer),
    Column('Name_Flora_Main_Species_3', Unicode(255)),
    Column('Id_Flora_Main_Species_3', Integer),
    Column('Vegetation_cover', Integer),
    Column('Perennial_cover', Integer),
    Column('Comments', Unicode(255)),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('Cultivated_1', BIT, nullable=False),
    Column('Cultivated_2', BIT, nullable=False),
    Column('Cultivated_3', BIT, nullable=False)
)


t_TProtocol_Station_Description = Table(
    'TProtocol_Station_Description', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer),
    Column('Id_Landscape', Integer),
    Column('Name_Landscape', Unicode(500)),
    Column('Id_VegetationType', Integer),
    Column('Name_VegetationType', Unicode(100)),
    Column('Name_Flora_Main_Species_1', Unicode),
    Column('Name_Flora_Main_Species_2', Unicode),
    Column('Name_Flora_Main_Species_3', Unicode),
    Column('Id_Substrat', Integer),
    Column('Name_Substrat', Unicode(250)),
    Column('Id_Topography', Integer),
    Column('Name_Topography', Unicode(250)),
    Column('Id_Exposition', Integer),
    Column('Name_Exposition', Unicode(250)),
    Column('Id_Slope_Class', Integer),
    Column('Name_Slope_Class', Unicode(250)),
    Column('Area', Float(53)),
    Column('Cover', Float(53)),
    Column('Id_Moisture', Integer),
    Column('Name_Moisture', Unicode(100)),
    Column('Id_Density_herbs', Integer),
    Column('Name_Density_herbs', Unicode(100)),
    Column('Id_Density_bushes', Integer),
    Column('Name_Density_bushes', Unicode(100)),
    Column('Id_Density_trees', Integer),
    Column('Name_Density_trees', Unicode(100)),
    Column('Id_Greeness_herbs', Integer),
    Column('Name_Greeness_herbs', Unicode(100)),
    Column('Id_Greeness_bushes', Integer),
    Column('Name_Greeness_bushes', Unicode(100)),
    Column('Id_Greeness_trees', Integer),
    Column('Name_Greeness_trees', Unicode(100)),
    Column('Phenology_Vegetative_herbs', BIT, nullable=False),
    Column('Phenology_Flowering_herbs', BIT, nullable=False),
    Column('Phenology_Seeding_herbs', BIT, nullable=False),
    Column('Phenology_Vegetative_bushes', BIT, nullable=False),
    Column('Phenology_Flowering_bushes', BIT, nullable=False),
    Column('Phenology_Seeding_bushes', BIT, nullable=False),
    Column('Phenology_Vegetative_trees', BIT, nullable=False),
    Column('Phenology_Flowering_trees', BIT, nullable=False),
    Column('Phenology_Seeding_trees', BIT, nullable=False),
    Column('Last_Rain_event', Unicode(100)),
    Column('Houbara_Suitable', BIT, nullable=False),
    Column('Comments', Text(collation='French_CI_AS'))
)


t_TProtocol_Station_equipment = Table(
    'TProtocol_Station_equipment', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('id_action_type', Integer, nullable=False),
    Column('name_action_type', Unicode(250), nullable=False),
    Column('id_sensor_type', Integer),
    Column('name_sensor_type', Unicode(250), nullable=False),
    Column('Comments', Unicode(255))
)


t_TProtocol_Track_clue = Table(
    'TProtocol_Track_clue', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('Id_Track_clue', Integer),
    Column('Name_Track_clue', Unicode(250)),
    Column('Comments', Unicode(255)),
    Column('id_taxon', Integer),
    Column('name_taxon', Unicode(250)),
    Column('Identity_sure', BIT, nullable=False),
    Column('Number_Track_clue', Integer),
    Column('Sampled', BIT, nullable=False)
)


t_TProtocol_Transects = Table(
    'TProtocol_Transects', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('Num_Bound', Integer),
    Column('Num_Transect', Integer),
    Column('Comments', Unicode(255)),
    Column('Id_Observer', Integer),
    Column('Id_Assistant', Integer)
)


t_TProtocol_Vertebrate_Group = Table(
    'TProtocol_Vertebrate_Group', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('Name_Taxon', Unicode(250)),
    Column('Id_Taxon', Integer, nullable=False),
    Column('Identity_sure', BIT, nullable=False),
    Column('Ident_Occasional', BIT, nullable=False),
    Column('Nb_Adult_Male', Integer),
    Column('Nb_Adult_Female', Integer),
    Column('Nb_Adult_Indeterminate', Integer),
    Column('Nb_Juvenile_Male', Integer),
    Column('Nb_Juvenile_Female', Integer),
    Column('Nb_Juvenile_Indeterminate', Integer),
    Column('Nb_NewBorn_Male', Integer),
    Column('Nb_NewBorn_Female', Integer),
    Column('Nb_NewBorn_Indeterminate', Integer),
    Column('Nb_Indeterminate', Integer),
    Column('Name_Behaviour', Unicode(250)),
    Column('Id_Behaviour', Integer),
    Column('Disturbed', BIT, nullable=False),
    Column('Comments', Unicode(300)),
    Column('Measured_Distance', Numeric(9, 2)),
    Column('AngleNorth', Numeric(9, 2)),
    Column('Estimated_Distance', Numeric(9, 2)),
    Column('AngleTrack', Numeric(9, 2)),
    Column('Nb_Total', Integer),
    Column('timestamp', DateTime, nullable=False),
    Column('observation_time', DateTime)
)


t_TProtocol_Vertebrate_Individual = Table(
    'TProtocol_Vertebrate_Individual', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('Fk_TInd_ID', Integer),
    Column('Fk_Group', Integer),
    Column('frequency', Integer),
    Column('id_sex', Integer),
    Column('name_sex', Unicode(50)),
    Column('id_age', Integer),
    Column('name_age', Unicode(50)),
    Column('Id_signal_type', Integer),
    Column('Name_signal_type', Unicode(250)),
    Column('Id_Posture', Integer),
    Column('Name_Posture', Unicode(250)),
    Column('Id_Behaviour', Integer),
    Column('Name_Behaviour', Unicode(250)),
    Column('Identification_type', String(10, 'French_CI_AS')),
    Column('Identification_criteria', Unicode(500)),
    Column('Comments', Unicode(540)),
    Column('Sampled', BIT),
    Column('Disturbed', BIT),
    Column('timestamp', DateTime, nullable=False)
)


t_TProtocol_Vertebrate_Individual_Death = Table(
    'TProtocol_Vertebrate_Individual_Death', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('FK_TInd_ID', Integer),
    Column('Id_Remains', Integer),
    Column('Name_Remains', Unicode(250)),
    Column('Id_Death_Time', Integer),
    Column('Name_Death_Time', Unicode(250)),
    Column('Id_Death_Reason', Integer),
    Column('Name_Death_Reason', Unicode(250)),
    Column('Identification_criteria', Unicode(500)),
    Column('Sure_reason', BIT, nullable=False),
    Column('Identification_type', Unicode(10)),
    Column('Comments', Unicode(500)),
    Column('Name_Taxon', Unicode(255)),
    Column('Id_Taxon', Integer),
    Column('Sampled', BIT, nullable=False)
)


t_TProtocol_Vertebrate_interview = Table(
    'TProtocol_Vertebrate_interview', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_TSta_ID', Integer, nullable=False),
    Column('Name_InterviewType', Unicode(250)),
    Column('Id_InterviewType', Integer),
    Column('Name_Taxon', Unicode(250)),
    Column('Id_Taxon', Integer),
    Column('Identity_sure', BIT, nullable=False),
    Column('Nb_Adult_Male', Integer),
    Column('Nb_Adult_Female', Integer),
    Column('Nb_Adult_Indeterminate', Integer),
    Column('Nb_Juvenile_Male', Integer),
    Column('Nb_Juvenile_Female', Integer),
    Column('Nb_Juvenile_Indeterminate', Integer),
    Column('Nb_NewBorn_Male', Integer),
    Column('Nb_NewBorn_Female', Integer),
    Column('Nb_NewBorn_Indeterminate', Integer),
    Column('Nb_Indeterminate', Integer),
    Column('Name_Behaviour', Unicode(250)),
    Column('Id_Behaviour', Integer),
    Column('Observer', Unicode(255)),
    Column('Comments', Unicode(255))
)


class TProtocole(Base):
    __tablename__ = 'TProtocole'

    TTheEt_PK_ID = Column(Integer, primary_key=True)
    Relation = Column(String(collation='French_CI_AS'))
    Caption = Column(String(collation='French_CI_AS'))
    Description = Column(String(collation='French_CI_AS'))
    Creation_date = Column(DateTime)
    Creator = Column(String(collation='French_CI_AS'))
    Support = Column(String(collation='French_CI_AS'))


t_TQryAdminDB = Table(
    'TQryAdminDB', metadata,
    Column('TQryAdminDB_ID', Integer, nullable=False),
    Column('TQryAdminDB_sp_name', Unicode(300)),
    Column('TQryAdminDB_Layer_Name', Unicode(50)),
    Column('TQryAdminDB_Description', Unicode(200))
)


class TStation(Base):
    __tablename__ = 'TStations'

    TSta_PK_ID = Column(Integer, primary_key=True, index=True)
    FieldWorker1 = Column(Integer)
    FieldWorker2 = Column(Integer)
    FieldWorker3 = Column(Integer)
    NbFieldWorker = Column(Integer)
    FieldActivity_ID = Column(Integer)
    FieldActivity_Name = Column(Unicode(255))
    Name = Column(Unicode(255))
    Region = Column(Unicode(255))
    Place = Column(Unicode(50))
    DATE = Column(DateTime)
    LAT = Column(Numeric(9, 5))
    LON = Column(Numeric(9, 5))
    Precision = Column(Integer)
    ELE = Column(Integer)
    Creator = Column(Integer)
    Creation_date = Column(DateTime)
    TSta_FK_TGeo_ID = Column(Integer)
    Id_DistanceFromObs = Column(Integer)
    Name_DistanceFromObs = Column(Unicode(200))
    Comments = Column(Unicode(250))
    UTM20 = Column(Unicode(50))
    timestamp = Column(DateTime, nullable=False)
    regionUpdate = Column(BIT, nullable=False)


t_TSubProtocol_Entomo_Pop_Census = Table(
    'TSubProtocol_Entomo_Pop_Census', metadata,
    Column('PK', Integer, nullable=False),
    Column('FK_Pr', Integer, nullable=False),
    Column('Id_Taxon', Integer, nullable=False),
    Column('Name_Taxon', Unicode(1000), nullable=False),
    Column('Identity_sure', BIT, nullable=False),
    Column('Identificator', Unicode(250)),
    Column('Year_identification', Date),
    Column('Validator', Unicode(250)),
    Column('Year_validation', Date),
    Column('Collected', BIT, nullable=False),
    Column('Collected_label', Unicode(250)),
    Column('Id_Behaviour', Integer),
    Column('Name_Behaviour', Unicode(250)),
    Column('Male_adult_nb', Integer),
    Column('Female_adult_nb', Integer),
    Column('Indeterminate_adult_nb', Integer),
    Column('Indeterminate_pupa_nb', Integer),
    Column('Male_larva_nb', Integer),
    Column('Female_larva_nb', Integer),
    Column('Indeterminate_larva_nb', Integer),
    Column('Indeterminate_neonata_nb', Integer),
    Column('Indeterminate_egg_nb', Integer),
    Column('Id_Male_adult_ab', Integer),
    Column('Name_Male_adult_ab', Unicode(50)),
    Column('Id_Female_adult_ab', Integer),
    Column('Name_Female_adult_ab', Unicode(50)),
    Column('Id_Indeterminate_adult_ab', Integer),
    Column('Name_Indeterminate_adult_ab', Unicode(50)),
    Column('Id_Indeterminate_pupa_ab', Integer),
    Column('Name_Indeterminate_pupa_ab', Unicode(50)),
    Column('Id_Male_larva_ab', Integer),
    Column('Name_Male_larva_ab', Unicode(50)),
    Column('Id_Female_larva_ab', Integer),
    Column('Name_Female_larva_ab', Unicode(50)),
    Column('Id_Indeterminate_larva_ab', Integer),
    Column('Name_Indeterminate_larva_ab', Unicode(50)),
    Column('Id_Indeterminate_neonata_ab', Integer),
    Column('Name_Indeterminate_neonata_ab', Unicode(50)),
    Column('Id_Indeterminate_egg_ab', Integer),
    Column('Name_Indeterminate_egg_ab', Unicode(50)),
    Column('Comments', Unicode(250))
)


t_TSubProtocol_Transect = Table(
    'TSubProtocol_Transect', metadata,
    Column('PK', Integer, nullable=False),
    Column('Fk_Trans', Integer),
    Column('Id_Taxon', Integer, nullable=False),
    Column('Name_Taxon', Unicode(1000), nullable=False),
    Column('P1', Integer),
    Column('P2', Integer),
    Column('P3', Integer),
    Column('P4', Integer),
    Column('P5', Integer),
    Column('P6', Integer),
    Column('P7', Integer),
    Column('P8', Integer),
    Column('P9', Integer),
    Column('P10', Integer),
    Column('P11', Integer),
    Column('P12', Integer),
    Column('P13', Integer),
    Column('P14', Integer),
    Column('P15', Integer),
    Column('P16', Integer),
    Column('P17', Integer),
    Column('P18', Integer),
    Column('P19', Integer),
    Column('P20', Integer),
    Column('P21', Integer),
    Column('P22', Integer),
    Column('P23', Integer),
    Column('P24', Integer),
    Column('P25', Integer),
    Column('P26', Integer),
    Column('P27', Integer),
    Column('P28', Integer),
    Column('P29', Integer),
    Column('P30', Integer),
    Column('P31', Integer),
    Column('P32', Integer),
    Column('P33', Integer),
    Column('P34', Integer),
    Column('P35', Integer),
    Column('P36', Integer),
    Column('P37', Integer),
    Column('P38', Integer),
    Column('P39', Integer),
    Column('P40', Integer),
    Column('P41', Integer),
    Column('P42', Integer),
    Column('P43', Integer),
    Column('P44', Integer),
    Column('P45', Integer),
    Column('P46', Integer),
    Column('P47', Integer),
    Column('P48', Integer),
    Column('P49', Integer),
    Column('P50', Integer),
    Column('P51', Integer),
    Column('P52', Integer),
    Column('P53', Integer),
    Column('P54', Integer),
    Column('P55', Integer),
    Column('P56', Integer),
    Column('P57', Integer),
    Column('P58', Integer),
    Column('P59', Integer),
    Column('P60', Integer),
    Column('P61', Integer),
    Column('P62', Integer),
    Column('P63', Integer),
    Column('P64', Integer),
    Column('P65', Integer),
    Column('P66', Integer),
    Column('P67', Integer),
    Column('P68', Integer),
    Column('P69', Integer),
    Column('P70', Integer),
    Column('P71', Integer),
    Column('P72', Integer),
    Column('P73', Integer),
    Column('P74', Integer),
    Column('P75', Integer),
    Column('P76', Integer),
    Column('P77', Integer),
    Column('P78', Integer),
    Column('P79', Integer),
    Column('P80', Integer),
    Column('P81', Integer),
    Column('P82', Integer),
    Column('P83', Integer),
    Column('P84', Integer),
    Column('P85', Integer),
    Column('P86', Integer),
    Column('P87', Integer),
    Column('P88', Integer),
    Column('P89', Integer),
    Column('P90', Integer),
    Column('P91', Integer),
    Column('P92', Integer),
    Column('P93', Integer),
    Column('P94', Integer),
    Column('P95', Integer),
    Column('P96', Integer),
    Column('P97', Integer),
    Column('P98', Integer),
    Column('P99', Integer),
    Column('P100', Integer),
    Column('P101', Integer),
    Column('P102', Integer),
    Column('P103', Integer),
    Column('P104', Integer),
    Column('P105', Integer),
    Column('P106', Integer),
    Column('P107', Integer),
    Column('P108', Integer),
    Column('P109', Integer),
    Column('P110', Integer),
    Column('P111', Integer),
    Column('P112', Integer),
    Column('P113', Integer),
    Column('P114', Integer),
    Column('P115', Integer),
    Column('P116', Integer),
    Column('P117', Integer),
    Column('P118', Integer),
    Column('P119', Integer),
    Column('P120', Integer),
    Column('P121', Integer),
    Column('P122', Integer),
    Column('P123', Integer),
    Column('P124', Integer),
    Column('P125', Integer),
    Column('P126', Integer),
    Column('P127', Integer),
    Column('P128', Integer),
    Column('P129', Integer),
    Column('P130', Integer),
    Column('P131', Integer),
    Column('P132', Integer),
    Column('P133', Integer),
    Column('P134', Integer),
    Column('P135', Integer),
    Column('P136', Integer),
    Column('P137', Integer),
    Column('P138', Integer),
    Column('P139', Integer),
    Column('P140', Integer),
    Column('P141', Integer),
    Column('P142', Integer),
    Column('P143', Integer),
    Column('P144', Integer),
    Column('P145', Integer),
    Column('P146', Integer),
    Column('P147', Integer),
    Column('P148', Integer),
    Column('P149', Integer),
    Column('P150', Integer),
    Column('P151', Integer),
    Column('P152', Integer),
    Column('P153', Integer),
    Column('P154', Integer),
    Column('P155', Integer),
    Column('P156', Integer),
    Column('P157', Integer),
    Column('P158', Integer),
    Column('P159', Integer),
    Column('P160', Integer),
    Column('P161', Integer),
    Column('P162', Integer),
    Column('P163', Integer),
    Column('P164', Integer),
    Column('P165', Integer),
    Column('P166', Integer),
    Column('P167', Integer),
    Column('P168', Integer),
    Column('P169', Integer),
    Column('P170', Integer),
    Column('P171', Integer),
    Column('P172', Integer),
    Column('P173', Integer),
    Column('P174', Integer),
    Column('P175', Integer),
    Column('P176', Integer),
    Column('P177', Integer),
    Column('P178', Integer),
    Column('P179', Integer),
    Column('P180', Integer),
    Column('P181', Integer),
    Column('P182', Integer),
    Column('P183', Integer),
    Column('P184', Integer),
    Column('P185', Integer),
    Column('P186', Integer),
    Column('P187', Integer),
    Column('P188', Integer),
    Column('P189', Integer),
    Column('P190', Integer),
    Column('P191', Integer),
    Column('P192', Integer),
    Column('P193', Integer),
    Column('P194', Integer),
    Column('P195', Integer),
    Column('P196', Integer),
    Column('P197', Integer),
    Column('P198', Integer),
    Column('P199', Integer),
    Column('P200', Integer),
    Column('Identity_sure', BIT, nullable=False),
    Column('Validator', Integer),
    Column('Sampled', BIT, nullable=False),
    Column('Picture', BIT, nullable=False),
    Column('Cultivated', BIT, nullable=False),
    Column('Comments', Unicode(250)),
    Column('nb_contact', Integer),
    Column('timestamp', DateTime, nullable=False)
)


t_TTEMP_Objects_2_import = Table(
    'TTEMP_Objects_2_import', metadata,
    Column('begin_date', DateTime),
    Column('id5@TCarac_Transmitter_Frequency', Numeric(18, 0)),
    Column('id42@TCaracThes_Company', Numeric(18, 0)),
    Column('id42@TCaracThes_Company_Precision', String(50, 'French_CI_AS')),
    Column('id41@TCaracThes_Model', Numeric(18, 0)),
    Column('id41@TCaracThes_Model_Precision', String(50, 'French_CI_AS')),
    Column('id43@TCarac_Weight', Numeric(18, 0)),
    Column('id44@TCarac_InitialLivespan', Numeric(18, 0)),
    Column('id6@TCarac_Transmitter_Serial_Number', String(50, 'French_CI_AS')),
    Column('id1@Thes_Status', Numeric(18, 0)),
    Column('id1@Thes_Status_Precision', String(50, 'French_CI_AS')),
    Column('id46@TCaracThes_BatteryType_Precision', String(50, 'French_CI_AS')),
    Column('id46@TCaracThes_BatteryType', Numeric(18, 0)),
    Column('id40@TCaracThes_Shape_Precision', String(50, 'French_CI_AS')),
    Column('id40@TCaracThes_Shape', Numeric(18, 0)),
    Column('object_type', String(50, 'French_CI_AS')),
    Column('PK', Integer, nullable=False)
)


t_TTempCheckGazel = Table(
    'TTempCheckGazel', metadata,
    Column('Name', String(50, 'French_CI_AS')),
    Column('LAT', Numeric(7, 5)),
    Column('Lon', Numeric(7, 5)),
    Column('Date', DateTime)
)


t_TTempTViewIndivBack = Table(
    'TTempTViewIndivBack', metadata,
    Column('Individual_Obj_PK', Integer, nullable=False),
    Column('id2@Thes_Age', Integer),
    Column('id2@Thes_Age_Precision', Unicode(150)),
    Column('id3@TCaracThes_Transmitter_Shape', Integer),
    Column('id3@TCaracThes_Transmitter_Shape_Precision', Unicode(150)),
    Column('id4@TCaracThes_Transmitter_Model', Integer),
    Column('id4@TCaracThes_Transmitter_Model_Precision', Unicode(150)),
    Column('id5@TCarac_Transmitter_Frequency', Integer),
    Column('id6@TCarac_Transmitter_Serial_Number', Unicode(100)),
    Column('id7@TCaracThes_Release_Ring_Position', Integer),
    Column('id7@TCaracThes_Release_Ring_Position_Precision', Unicode(150)),
    Column('id8@TCaracThes_Release_Ring_Color', Integer),
    Column('id8@TCaracThes_Release_Ring_Color_Precision', Unicode(150)),
    Column('id9@TCarac_Release_Ring_Code', Unicode(100)),
    Column('id10@TCaracThes_Breeding_Ring_Position', Integer),
    Column('id10@TCaracThes_Breeding_Ring_Position_Precision', Unicode(150)),
    Column('id11@TCaracThes_Breeding_Ring_Color', Integer),
    Column('id11@TCaracThes_Breeding_Ring_Color_Precision', Unicode(150)),
    Column('id12@TCarac_Breeding_Ring_Code', Unicode(100)),
    Column('id13@TCarac_Chip_Code', Unicode(100)),
    Column('id14@TCaracThes_Mark_Color_1', Integer),
    Column('id14@TCaracThes_Mark_Color_1_Precision', Unicode(150)),
    Column('id15@TCaracThes_Mark_Position_1', Integer),
    Column('id15@TCaracThes_Mark_Position_1_Precision', Unicode(150)),
    Column('id16@TCaracThes_Mark_Color_2', Integer),
    Column('id16@TCaracThes_Mark_Color_2_Precision', Unicode(150)),
    Column('id17@TCaracThes_Mark_Position_2', Integer),
    Column('id17@TCaracThes_Mark_Position_2_Precision', Unicode(150)),
    Column('id19@TCarac_PTT', Integer),
    Column('id20@TCaracThes_PTT_manufacturer', Integer),
    Column('id20@TCaracThes_PTT_manufacturer_Precision', Unicode(150)),
    Column('id22@TCaracThes_PTT_model', Integer),
    Column('id22@TCaracThes_PTT_model_Precision', Unicode(150)),
    Column('id30@TCaracThes_Sex', Integer),
    Column('id30@TCaracThes_Sex_Precision', Unicode(150)),
    Column('id33@Thes_Origin', Integer),
    Column('id33@Thes_Origin_Precision', Unicode(150)),
    Column('id34@TCaracThes_Species', Integer),
    Column('id34@TCaracThes_Species_Precision', Unicode(150)),
    Column('id35@Birth_date', DateTime),
    Column('id36@Death_date', DateTime),
    Column('id37@Comments', Unicode(255)),
    Column('id55@TCarac_Mark_code_1', Unicode(100)),
    Column('id56@TCarac_Mark_code_2', Unicode(100)),
    Column('id59@TCaracThes_Individual_Status', Unicode(250)),
    Column('id60@TCaracThes_Monitoring_Status', Integer),
    Column('id60@TCaracThes_Monitoring_Status_Precision', Unicode(150)),
    Column('id61@TCaracThes_Survey_type', Integer),
    Column('id61@TCaracThes_Survey_type_Precision', Unicode(150))
)


t_TThemeEtude = Table(
    'TThemeEtude', metadata,
    Column('TProt_PK_ID', Integer, nullable=False),
    Column('Caption', Unicode(50)),
    Column('Definition_fr', Unicode(250)),
    Column('Bibliography', Unicode(250)),
    Column('Creation_date', DateTime),
    Column('Creator', Unicode(50)),
    Column('Actif', BIT, nullable=False),
    Column('NeedGeom', BIT, nullable=False),
    Column('Definition_en', Unicode(250))
)


class TViewIndividual(Base):
    __tablename__ = 'TViewIndividual'

    Individual_Obj_PK = Column(Integer, primary_key=True)
    id2_Thes_Age = Column('id2@Thes_Age', Integer)
    id2_Thes_Age_Precision = Column('id2@Thes_Age_Precision', Unicode(150))
    id3_TCaracThes_Transmitter_Shape = Column('id3@TCaracThes_Transmitter_Shape', Integer)
    id3_TCaracThes_Transmitter_Shape_Precision = Column('id3@TCaracThes_Transmitter_Shape_Precision', Unicode(150))
    id4_TCaracThes_Transmitter_Model = Column('id4@TCaracThes_Transmitter_Model', Integer)
    id4_TCaracThes_Transmitter_Model_Precision = Column('id4@TCaracThes_Transmitter_Model_Precision', Unicode(150))
    id5_TCarac_Transmitter_Frequency = Column('id5@TCarac_Transmitter_Frequency', Integer)
    id6_TCarac_Transmitter_Serial_Number = Column('id6@TCarac_Transmitter_Serial_Number', Unicode(100))
    id7_TCaracThes_Release_Ring_Position = Column('id7@TCaracThes_Release_Ring_Position', Integer)
    id7_TCaracThes_Release_Ring_Position_Precision = Column('id7@TCaracThes_Release_Ring_Position_Precision', Unicode(150))
    id8_TCaracThes_Release_Ring_Color = Column('id8@TCaracThes_Release_Ring_Color', Integer)
    id8_TCaracThes_Release_Ring_Color_Precision = Column('id8@TCaracThes_Release_Ring_Color_Precision', Unicode(150))
    id9_TCarac_Release_Ring_Code = Column('id9@TCarac_Release_Ring_Code', Unicode(100))
    id10_TCaracThes_Breeding_Ring_Position = Column('id10@TCaracThes_Breeding_Ring_Position', Integer)
    id10_TCaracThes_Breeding_Ring_Position_Precision = Column('id10@TCaracThes_Breeding_Ring_Position_Precision', Unicode(150))
    id11_TCaracThes_Breeding_Ring_Color = Column('id11@TCaracThes_Breeding_Ring_Color', Integer)
    id11_TCaracThes_Breeding_Ring_Color_Precision = Column('id11@TCaracThes_Breeding_Ring_Color_Precision', Unicode(150))
    id12_TCarac_Breeding_Ring_Code = Column('id12@TCarac_Breeding_Ring_Code', Unicode(100))
    id13_TCarac_Chip_Code = Column('id13@TCarac_Chip_Code', Unicode(100))
    id14_TCaracThes_Mark_Color_1 = Column('id14@TCaracThes_Mark_Color_1', Integer)
    id14_TCaracThes_Mark_Color_1_Precision = Column('id14@TCaracThes_Mark_Color_1_Precision', Unicode(150))
    id15_TCaracThes_Mark_Position_1 = Column('id15@TCaracThes_Mark_Position_1', Integer)
    id15_TCaracThes_Mark_Position_1_Precision = Column('id15@TCaracThes_Mark_Position_1_Precision', Unicode(150))
    id16_TCaracThes_Mark_Color_2 = Column('id16@TCaracThes_Mark_Color_2', Integer)
    id16_TCaracThes_Mark_Color_2_Precision = Column('id16@TCaracThes_Mark_Color_2_Precision', Unicode(150))
    id17_TCaracThes_Mark_Position_2 = Column('id17@TCaracThes_Mark_Position_2', Integer)
    id17_TCaracThes_Mark_Position_2_Precision = Column('id17@TCaracThes_Mark_Position_2_Precision', Unicode(150))
    id19_TCarac_PTT = Column('id19@TCarac_PTT', Integer)
    id20_TCaracThes_PTT_manufacturer = Column('id20@TCaracThes_PTT_manufacturer', Integer)
    id20_TCaracThes_PTT_manufacturer_Precision = Column('id20@TCaracThes_PTT_manufacturer_Precision', Unicode(150))
    id22_TCaracThes_PTT_model = Column('id22@TCaracThes_PTT_model', Integer)
    id22_TCaracThes_PTT_model_Precision = Column('id22@TCaracThes_PTT_model_Precision', Unicode(150))
    id30_TCaracThes_Sex = Column('id30@TCaracThes_Sex', Integer)
    id30_TCaracThes_Sex_Precision = Column('id30@TCaracThes_Sex_Precision', Unicode(150))
    id33_Thes_Origin = Column('id33@Thes_Origin', Integer)
    id33_Thes_Origin_Precision = Column('id33@Thes_Origin_Precision', Unicode(150))
    id34_TCaracThes_Species = Column('id34@TCaracThes_Species', Integer)
    id34_TCaracThes_Species_Precision = Column('id34@TCaracThes_Species_Precision', Unicode(150), index=True)
    id35_Birth_date = Column('id35@Birth_date', DateTime)
    id36_Death_date = Column('id36@Death_date', DateTime)
    id37_Comments = Column('id37@Comments', Unicode(255))
    id55_TCarac_Mark_code_1 = Column('id55@TCarac_Mark_code_1', Unicode(100))
    id56_TCarac_Mark_code_2 = Column('id56@TCarac_Mark_code_2', Unicode(100))
    id59_TCaracThes_Individual_Status = Column('id59@TCaracThes_Individual_Status', Unicode(250))
    id60_TCaracThes_Monitoring_Status = Column('id60@TCaracThes_Monitoring_Status', Integer)
    id60_TCaracThes_Monitoring_Status_Precision = Column('id60@TCaracThes_Monitoring_Status_Precision', Unicode(150))
    id61_TCaracThes_Survey_type = Column('id61@TCaracThes_Survey_type', Integer)
    id61_TCaracThes_Survey_type_Precision = Column('id61@TCaracThes_Survey_type_Precision', Unicode(150))


class TViewRFID(Base):
    __tablename__ = 'TViewRFID'

    RFID_Obj_pk = Column(Integer, primary_key=True)
    id65_TCarac_rfid_Serial_number = Column('id65@TCarac_rfid_Serial_number', Integer)
    id41_TCaracThes_Model = Column('id41@TCaracThes_Model', Integer)
    id41_TCaracThes_Model_Precision = Column('id41@TCaracThes_Model_Precision', String(50, 'French_CI_AS'))
    id42_TCaracThes_Company = Column('id42@TCaracThes_Company', Integer)
    id42_TCaracThes_Company_Precision = Column('id42@TCaracThes_Company_Precision', String(50, 'French_CI_AS'))
    id37_Comments = Column('id37@Comments', String(collation='French_CI_AS'))


t_TViewTrx_Radio = Table(
    'TViewTrx_Radio', metadata,
    Column('Trx_Radio_Obj_PK', Integer, nullable=False),
    Column('id1@Thes_Status', Integer),
    Column('id1@Thes_Status_Precision', Unicode(150)),
    Column('id5@TCarac_Transmitter_Frequency', Integer),
    Column('id6@TCarac_Transmitter_Serial_Number', Unicode(100)),
    Column('id24@TCaracThes_Txt_Harness', Integer),
    Column('id24@TCaracThes_Txt_Harness_Precision', Unicode(150)),
    Column('id37@Comments', Unicode(255)),
    Column('id40@TCaracThes_Shape', Integer),
    Column('id40@TCaracThes_Shape_Precision', Unicode(150)),
    Column('id41@TCaracThes_Model', Integer),
    Column('id41@TCaracThes_Model_Precision', Unicode(150)),
    Column('id42@TCaracThes_Company', Integer),
    Column('id42@TCaracThes_Company_Precision', Unicode(150)),
    Column('id43@TCarac_Weight', Float(53)),
    Column('id44@TCarac_InitialLivespan', Integer),
    Column('id46@TCaracThes_BatteryType', Integer),
    Column('id46@TCaracThes_BatteryType_Precision', Unicode(150)),
    Column('id57@TCarac_UpdatedLifeSpan', Integer),
    Column('id58@TCarac_Date_UpdatedLifeSpan', DateTime)
)


t_TViewTrx_Sat = Table(
    'TViewTrx_Sat', metadata,
    Column('Trx_Sat_Obj_PK', Integer, nullable=False),
    Column('id1@Thes_Status', Integer),
    Column('id1@Thes_Status_Precision', Unicode(150)),
    Column('id6@TCarac_Transmitter_Serial_Number', Unicode(100)),
    Column('id19@TCarac_PTT', Integer),
    Column('id24@TCaracThes_Txt_Harness', Integer),
    Column('id24@TCaracThes_Txt_Harness_Precision', Unicode(150)),
    Column('id25@TCaracThes_Txt_Argos_DutyCycle', Integer),
    Column('id25@TCaracThes_Txt_Argos_DutyCycle_Precision', Unicode(150)),
    Column('id37@Comments', Unicode(255)),
    Column('id41@TCaracThes_Model', Integer),
    Column('id41@TCaracThes_Model_Precision', Unicode(150)),
    Column('id42@TCaracThes_Company', Integer),
    Column('id42@TCaracThes_Company_Precision', Unicode(150)),
    Column('id43@TCarac_Weight', Float(53)),
    Column('id44@TCarac_InitialLivespan', Integer),
    Column('id49@TCarac_PTTAssignmentDate', DateTime)
)


class TAnimal(Base):
    __tablename__ = 'T_Animal'
    __table_args__ = (
        Index('idx_Tanimal_chipcode_pk', 'chip_code', 'PK_id'),
    )

    PK_id = Column(Integer, primary_key=True)
    chip_code = Column(String(10, 'French_CI_AS'))


class TAnimalLocation(Base):
    __tablename__ = 'T_AnimalLocation'
    __table_args__ = (
        Index('idx_Tanimallocation_ind_date_with_lat_lon', 'FK_ind', 'date_', 'lat', 'lon'),
    )

    PK_id = Column(Integer, primary_key=True)
    FK_creator = Column(ForeignKey('T_User.PK_id'), nullable=False)
    FK_obj = Column(ForeignKey('T_Object.PK_id'), nullable=False)
    FK_ind = Column(Integer, nullable=False)
    type_ = Column(String(8, 'French_CI_AS'))
    date_ = Column(DateTime, nullable=False)
    lat = Column(Numeric(9, 5), nullable=False)
    lon = Column(Numeric(9, 5), nullable=False)
    creation_date = Column(DateTime, server_default=text("(getdate())"))

    T_User = relationship('TUser')
    T_Object = relationship('TObject')


class TDataGsm(Base):
    __tablename__ = 'T_DataGsm'
    __table_args__ = (
        Index('UQ__T_DataGs__274D7756CAE3623D', 'platform_', 'date_', unique=True),
        Index('idx_Tdatagsm_platform_checked_with_date_lat_lon_ele', 'platform_', 'checked', 'date_', 'lat', 'lon', 'ele')
    )

    PK_id = Column(Integer, primary_key=True)
    platform_ = Column(Integer, nullable=False)
    date_ = Column(DateTime, nullable=False)
    lat = Column(Numeric(9, 5), nullable=False)
    lon = Column(Numeric(9, 5), nullable=False)
    ele = Column(Integer)
    speed = Column(Integer)
    course = Column(Integer)
    hdop = Column(Float(53))
    vdop = Column(Float(53))
    sat_count = Column(Integer)
    checked = Column(BIT, nullable=False, server_default=text("('0')"))
    imported = Column(BIT, nullable=False, server_default=text("('0')"))


class TDataRfid(Base):
    __tablename__ = 'T_DataRfid'
    __table_args__ = (
        Index('UQ__T_DataRf__89DC9B4963077481', 'FK_obj', 'chip_code', 'date_', unique=True),
        Index('idx_Tdatarfid_chipcode_date', 'chip_code', 'date_')
    )

    PK_id = Column(Integer, primary_key=True)
    FK_creator = Column(ForeignKey('T_User.PK_id'))
    FK_obj = Column(ForeignKey('T_Object.PK_id'), nullable=False)
    chip_code = Column(String(10, 'French_CI_AS'), nullable=False)
    date_ = Column(DateTime, nullable=False)
    creation_date = Column(DateTime, server_default=text("(getdate())"))
    validated = Column(BIT, server_default=text("('0')"))

    T_User = relationship('TUser')
    T_Object = relationship('TObject')


class TMonitoredSite(Base):
    __tablename__ = 'T_MonitoredSite'

    PK_id = Column(Integer, primary_key=True)
    FK_creator = Column(ForeignKey('T_User.PK_id'))
    FK_type = Column(ForeignKey('T_Thesaurus.topic_en'))
    name = Column(String(50, 'French_CI_AS'), index=True)
    creation_date = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    active = Column(BIT)

    T_User = relationship('TUser')
    T_Thesauru = relationship('TThesauru')


class TMonitoredSiteEquipment(Base):
    __tablename__ = 'T_MonitoredSiteEquipment'

    PK_id = Column(Integer, primary_key=True)
    FK_obj = Column(ForeignKey('T_Object.PK_id'), nullable=False)
    FK_site = Column(ForeignKey('TMonitoredStations.TGeo_pk_id'), nullable=False)
    FK_creator = Column(ForeignKey('T_User.PK_id'), nullable=False)
    creation_date = Column(DateTime, server_default=text("(getdate())"))
    lat = Column(Numeric(9, 5), nullable=False)
    lon = Column(Numeric(9, 5), nullable=False)
    begin_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)

    T_User = relationship('TUser')
    T_Object = relationship('TObject')
    TMonitoredStation = relationship('TMonitoredStation')


class TObject(Base):
    __tablename__ = 'T_Object'
    __table_args__ = (
        Index('idx_Tobject_type', 'type_', 'identifier'),
    )

    PK_id = Column(Integer, primary_key=True)
    FK_creator = Column(ForeignKey('T_User.PK_id'))
    identifier = Column(String(32, 'French_CI_AS'), nullable=False, unique=True)
    type_ = Column(String(16, 'French_CI_AS'), nullable=False)
    manufacturer = Column(String(32, 'French_CI_AS'))
    model = Column(String(32, 'French_CI_AS'))
    creation_date = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    program_id = Column(Integer)
    serial_number = Column(String(32, 'French_CI_AS'))
    platform_id = Column(Integer)

    T_User = relationship('TUser')


class TThesauru(Base):
    __tablename__ = 'T_Thesaurus'

    PK_id = Column(Integer, primary_key=True)
    FK_creator = Column(ForeignKey('T_User.PK_id'))
    FK_modifier = Column(ForeignKey('T_User.PK_id'))
    type_ = Column(Integer, nullable=False)
    parent = Column(Integer, nullable=False)
    hierarchy = Column(String(64, 'French_CI_AS'), nullable=False)
    topic_fr = Column(String(256, 'French_CI_AS'), nullable=False)
    topic_en = Column(String(256, 'French_CI_AS'), nullable=False, unique=True)
    definition_fr = Column(String(collation='French_CI_AS'))
    definition_en = Column(String(collation='French_CI_AS'))
    reference = Column(String(collation='French_CI_AS'))
    creation_date = Column(DateTime, server_default=text("(getdate())"))
    modification_date = Column(DateTime)

    T_User = relationship('TUser', primaryjoin='TThesauru.FK_creator == TUser.PK_id')
    T_User1 = relationship('TUser', primaryjoin='TThesauru.FK_modifier == TUser.PK_id')


class TUser(Base):
    __tablename__ = 'T_User'
    __table_args__ = (
        Index('idx_Tuser_lastname_firstname', 'lastname', 'firstname', 'PK_id'),
    )

    PK_id = Column(Integer, primary_key=True)
    lastname = Column(String(50, 'French_CI_AS'), nullable=False)
    firstname = Column(String(50, 'French_CI_AS'), nullable=False)
    creation_date = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    login_ = Column(String(collation='French_CI_AS'), nullable=False)
    password_ = Column(String(collation='French_CI_AS'), nullable=False)
    language_ = Column(String(2, 'French_CI_AS'))
    role_ = Column(String(16, 'French_CI_AS'), nullable=False)


t_Tthesaurus = Table(
    'Tthesaurus', metadata,
    Column('ID', Integer, nullable=False),
    Column('Id_Type', Float(53)),
    Column('Id_Parent', Integer),
    Column('hierarchy', Unicode(500)),
    Column('topic_fr', Unicode(255)),
    Column('topic_en', Unicode(255)),
    Column('definition_fr', Unicode),
    Column('definition_en', Unicode),
    Column('Reference', String(collation='French_CI_AS')),
    Column('FK_Creator', Float(53)),
    Column('Creation_date', DateTime),
    Column('FK_Contacts_Id_Modificateur', Unicode(255)),
    Column('Date_heure_modification', Unicode(255)),
    Column('available_EAU', BIT, nullable=False),
    Column('available_Morocco', BIT, nullable=False)
)


t_VAllUsersApplications = Table(
    'VAllUsersApplications', metadata,
    Column('TIns_PK_ID', Integer, nullable=False),
    Column('TIns_Label', String(250, 'French_CI_AS'), nullable=False),
    Column('TIns_ApplicationPath', String(500, 'French_CI_AS')),
    Column('TIns_ImagePath', String(500, 'French_CI_AS')),
    Column('TIns_IconePath', String(500, 'French_CI_AS')),
    Column('TIns_Theme', String(500, 'French_CI_AS')),
    Column('TIns_Database', String(500, 'French_CI_AS')),
    Column('TIns_Order', Integer),
    Column('TApp_Description', Unicode(255)),
    Column('TRol_Label', String(250, 'French_CI_AS'), nullable=False),
    Column('TUse_PK_ID', Integer, nullable=False)
)


t_VAllUserseReleveConnexion = Table(
    'VAllUserseReleveConnexion', metadata,
    Column('RoleID', Integer),
    Column('TUse_PK_ID', Integer, nullable=False),
    Column('TUse_Login', String(255, 'French_CI_AS'), nullable=False),
    Column('TUse_Password', String(50, 'French_CI_AS')),
    Column('TApp_Nom', String(250, 'French_CI_AS'), nullable=False)
)


t_VUsers = Table(
    'VUsers', metadata,
    Column('Id_Utilisateur', Integer, nullable=False),
    Column('Utilisateur', String(201, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_V_DB_Indivs_Stations_Ids = Table(
    'V_DB_Indivs_Stations_Ids', metadata,
    Column('StaType', String(11, 'French_CI_AS'), nullable=False),
    Column('StaType_ID', Integer, nullable=False),
    Column('Sta_ID', Integer),
    Column('Ind_ID', Integer)
)


t_V_Individuals_History = Table(
    'V_Individuals_History', metadata,
    Column('ind_id', Integer, nullable=False),
    Column('Fk_carac', Integer),
    Column('value', Unicode(1000)),
    Column('label', String(collation='French_CI_AS')),
    Column('begin_date', DateTime, nullable=False),
    Column('end_date', DateTime)
)


t_V_Individuals_LatLonDate = Table(
    'V_Individuals_LatLonDate', metadata,
    Column('ind_id', Integer),
    Column('lat', Numeric(9, 5)),
    Column('lon', Numeric(9, 5)),
    Column('date', DateTime),
    Column('type_', String(collation='French_CI_AS'))
)


t_V_Individuals_Stations = Table(
    'V_Individuals_Stations', metadata,
    Column('ind_id', Integer),
    Column('sta_id', Integer, nullable=False),
    Column('fk_sta_type', Integer, nullable=False)
)


t_V_Qry_AllHoubara_TrappingData = Table(
    'V_Qry_AllHoubara_TrappingData', metadata,
    Column('MSName', Unicode(50)),
    Column('Site_type', Unicode(200)),
    Column('MSID', Integer),
    Column('StaID', Integer, nullable=False),
    Column('StaName', Unicode(255)),
    Column('DATE', DateTime),
    Column('FW1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FW2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NBFW', Integer),
    Column('FA', Unicode(255)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Elevation', Integer),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('CGPK', Integer, nullable=False),
    Column('Name_Taxon', Unicode(255)),
    Column('Name_Capture_Method', Unicode(250)),
    Column('Nb_Individuals', Integer),
    Column('Nb_Operator', Integer),
    Column('Time_Begin', DateTime),
    Column('Time_End', DateTime),
    Column('Failure_reason', Unicode(255)),
    Column('CGComments', Unicode(255)),
    Column('CIPK', Integer),
    Column('FK_TInd_ID', Integer),
    Column('NewPTTGSM', Unicode(250)),
    Column('NewPTTGSMModel', Unicode(1000)),
    Column('NewVHF', Unicode(250)),
    Column('NewVHFModel', Unicode(1000)),
    Column('CurrentPTTGSM', Integer),
    Column('CurrentPTTGSMModel', Unicode(150)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('Sex', Unicode(150)),
    Column('Origin', Unicode(150)),
    Column('CurrentIndStatus', Unicode(250)),
    Column('CurrentMonStatus', Unicode(150)),
    Column('CurrentSvType', Unicode(150)),
    Column('BreRingCode', Unicode(100)),
    Column('RelRingCode', Unicode(100)),
    Column('ChipCode', Unicode(100)),
    Column('Time_Capture', DateTime),
    Column('Time_Release', DateTime),
    Column('CIObs', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CIAssis', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CIComments', Unicode(255)),
    Column('AgeAtTrapping', Unicode(100)),
    Column('SexAtTrapping', Unicode(100)),
    Column('Weight', Float(53)),
    Column('Tarso_Metatarsus', Float(53)),
    Column('Skull', Float(53)),
    Column('Wing', Float(53)),
    Column('BioObs', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('BioAssis', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('BioComment', String(1000, 'French_CI_AS')),
    Column('TrueBirthDate', DateTime)
)


t_V_Qry_AllIndiv_AllStations_old = Table(
    'V_Qry_AllIndiv_AllStations_old', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('CurrentPTTModel', Unicode(150)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('Sex', Unicode(150)),
    Column('BreedingRing', Unicode(100)),
    Column('ReleaseRing', Unicode(100)),
    Column('ChipCode', Unicode(100)),
    Column('Mark1Color', Unicode(150)),
    Column('Mark1Position', Unicode(150)),
    Column('Mark1Code', Integer),
    Column('Mark2Color', Unicode(150)),
    Column('Mark2Position', Unicode(150)),
    Column('Mark2Code', Integer),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('StaType', String(11, 'French_CI_AS'), nullable=False),
    Column('Sta_ID', Integer, nullable=False),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('FW1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FW2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FA_ID', Integer),
    Column('FA', Unicode(255)),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CreationDate', DateTime)
)


t_V_Qry_AllIndivs_AllStations = Table(
    'V_Qry_AllIndivs_AllStations', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('CurrentIndividualStatus', Unicode(250)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('CurrentPTTModel', Unicode(150)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('MonitoringStatus@Station', Unicode(1000)),
    Column('SurveyType@Station', Unicode(1000)),
    Column('Sex', Unicode(150)),
    Column('ReleaseRing', Unicode(100)),
    Column('Ring', Unicode(100)),
    Column('ChipCode', Unicode(100)),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('RelCaptSta_ID', Integer),
    Column('RelCaptStaType', String(7, 'French_CI_AS')),
    Column('RelCaptStaDate', DateTime),
    Column('RelCaptYear', Integer),
    Column('RelCaptRegion', Unicode(255)),
    Column('RelCaptPlace', Unicode(50)),
    Column('RelCaptLAT', Numeric(9, 5)),
    Column('RelCaptLON', Numeric(9, 5)),
    Column('StaType', String(11, 'French_CI_AS'), nullable=False),
    Column('Sta_ID', Integer, nullable=False),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('FW1', Integer),
    Column('FW2', Integer),
    Column('FA_ID', Integer),
    Column('FA', Unicode(255))
)


t_V_Qry_AllIndivs_Capture_FirstStation = Table(
    'V_Qry_AllIndivs_Capture_FirstStation', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('CurrentIndividualStatus', Unicode(250)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('CurrentPTTModel', Unicode(150)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('Sex', Unicode(150)),
    Column('BreedindRing', Unicode(100)),
    Column('ReleaseRing', Unicode(100)),
    Column('ChipCode', Unicode(100)),
    Column('Mark1Color', Unicode(150)),
    Column('Mark1Position', Unicode(150)),
    Column('Mark1Code', Unicode(100)),
    Column('Mark2Color', Unicode(150)),
    Column('Mark2Position', Unicode(150)),
    Column('Mark2Code', Unicode(100)),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('WeightGrs', Float(53)),
    Column('Skull', Float(53)),
    Column('Tarso_Metatarsus', Float(53)),
    Column('CaptMethod_ID', Integer),
    Column('CaptMethod', Unicode(250)),
    Column('CaptComments', Unicode(255)),
    Column('StaType', String(7, 'French_CI_AS'), nullable=False),
    Column('Sta_ID', Integer, nullable=False),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('DaysSinceFirstStation', Integer, nullable=False),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('FW1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FW2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FA_ID', Integer),
    Column('FA', Unicode(255)),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CreationDate', DateTime),
    Column('IndivComments', Unicode(100)),
    Column('BiometryWeight', Float(53)),
    Column('BiometryComments', String(1000, 'French_CI_AS')),
    Column('VertebrateIndivComments', Unicode(100)),
    Column('BioStation_ID', Integer)
)


t_V_Qry_AllIndivs_Equip@Station = Table(
    'V_Qry_AllIndivs_Equip@Station', metadata,
    Column('pr_PK', Integer, nullable=False),
    Column('Ind_ID', Integer, nullable=False),
    Column('Taxon_ID', Integer),
    Column('Taxon', Unicode(150)),
    Column('Origin_ID', Integer),
    Column('Origin', Unicode(150)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('SurveyType@Station', Unicode(1000)),
    Column('MonitoringStatus@Station', Unicode(1000)),
    Column('StaType', String(11, 'French_CI_AS'), nullable=False),
    Column('StaType_ID', Integer, nullable=False),
    Column('Sta_ID', Integer, nullable=False),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('SurveyTypeID@Current', Integer),
    Column('SurveyType@Current', Unicode(150)),
    Column('MonitoringStatusID@Current', Integer),
    Column('MonitoringStatus@Current', Unicode(150)),
    Column('IndividualStatus@Current', Unicode(250)),
    Column('freqOpti@Station', Integer)
)


t_V_Qry_AllIndivs_Equip@Station_backup = Table(
    'V_Qry_AllIndivs_Equip@Station_backup', metadata,
    Column('pr_PK', Integer, nullable=False),
    Column('Ind_ID', Integer, nullable=False),
    Column('Taxon_ID', Integer),
    Column('Taxon', Unicode(150)),
    Column('Origin_ID', Integer),
    Column('Origin', Unicode(150)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('SurveyType@Station', Unicode(1000)),
    Column('MonitoringStatus@Station', Unicode(1000)),
    Column('StaType', String(11, 'French_CI_AS'), nullable=False),
    Column('StaType_ID', Integer, nullable=False),
    Column('Sta_ID', Integer, nullable=False),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('SurveyTypeID@Current', Integer),
    Column('SurveyType@Current', Unicode(150)),
    Column('MonitoringStatusID@Current', Integer),
    Column('MonitoringStatus@Current', Unicode(150)),
    Column('IndividualStatus@Current', Unicode(250)),
    Column('freqOpti@Station', Integer)
)


t_V_Qry_AllIndivs_EquipmentData = Table(
    'V_Qry_AllIndivs_EquipmentData', metadata,
    Column('fk_object', Integer, nullable=False),
    Column('PTT_VHF', Unicode(250), nullable=False),
    Column('EquipType', String(3, 'French_CI_AS'), nullable=False),
    Column('begin_date', DateTime, nullable=False),
    Column('end_date', DateTime),
    Column('Individual_Obj_PK', Integer, nullable=False),
    Column('id59@TCaracThes_Individual_Status', Unicode(250)),
    Column('id61@TCaracThes_Survey_type_Precision', Unicode(150)),
    Column('id60@TCaracThes_Monitoring_Status_Precision', Unicode(150)),
    Column('id2@Thes_Age', Integer),
    Column('id2@Thes_Age_Precision', Unicode(150)),
    Column('id3@TCaracThes_Transmitter_Shape', Integer),
    Column('id3@TCaracThes_Transmitter_Shape_Precision', Unicode(150)),
    Column('id4@TCaracThes_Transmitter_Model', Integer),
    Column('id4@TCaracThes_Transmitter_Model_Precision', Unicode(150)),
    Column('id5@TCarac_Transmitter_Frequency', Integer),
    Column('id6@TCarac_Transmitter_Serial_Number', Unicode(100)),
    Column('id7@TCaracThes_Release_Ring_Position', Integer),
    Column('id7@TCaracThes_Release_Ring_Position_Precision', Unicode(150)),
    Column('id8@TCaracThes_Release_Ring_Color', Integer),
    Column('id8@TCaracThes_Release_Ring_Color_Precision', Unicode(150)),
    Column('id9@TCarac_Release_Ring_Code', Unicode(100)),
    Column('id10@TCaracThes_Breeding_Ring_Position', Integer),
    Column('id10@TCaracThes_Breeding_Ring_Position_Precision', Unicode(150)),
    Column('id11@TCaracThes_Breeding_Ring_Color', Integer),
    Column('id11@TCaracThes_Breeding_Ring_Color_Precision', Unicode(150)),
    Column('id12@TCarac_Breeding_Ring_Code', Unicode(100)),
    Column('id13@TCarac_Chip_Code', Unicode(100)),
    Column('id14@TCaracThes_Mark_Color_1', Integer),
    Column('id14@TCaracThes_Mark_Color_1_Precision', Unicode(150)),
    Column('id15@TCaracThes_Mark_Position_1', Integer),
    Column('id15@TCaracThes_Mark_Position_1_Precision', Unicode(150)),
    Column('id16@TCaracThes_Mark_Color_2', Integer),
    Column('id16@TCaracThes_Mark_Color_2_Precision', Unicode(150)),
    Column('id17@TCaracThes_Mark_Position_2', Integer),
    Column('id17@TCaracThes_Mark_Position_2_Precision', Unicode(150)),
    Column('id19@TCarac_PTT', Integer),
    Column('id20@TCaracThes_PTT_manufacturer', Integer),
    Column('id20@TCaracThes_PTT_manufacturer_Precision', Unicode(150)),
    Column('id22@TCaracThes_PTT_model', Integer),
    Column('id22@TCaracThes_PTT_model_Precision', Unicode(150)),
    Column('id30@TCaracThes_Sex', Integer),
    Column('id30@TCaracThes_Sex_Precision', Unicode(150)),
    Column('id33@Thes_Origin', Integer),
    Column('id33@Thes_Origin_Precision', Unicode(150)),
    Column('id34@TCaracThes_Species', Integer),
    Column('id34@TCaracThes_Species_Precision', Unicode(150)),
    Column('id35@Birth_date', DateTime),
    Column('id36@Death_date', DateTime),
    Column('id37@Comments', Unicode(255)),
    Column('id55@TCarac_Mark_code_1', Unicode(100)),
    Column('id56@TCarac_Mark_code_2', Unicode(100))
)


t_V_Qry_AllIndivs_FirstStation = Table(
    'V_Qry_AllIndivs_FirstStation', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentIndividualStatus', Unicode(250)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('CurrentPTTModel', Unicode(150)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('SurveyType@Station', Unicode(1000)),
    Column('MonitoringStatus@Station', Unicode(1000)),
    Column('freqOpti@Station', Integer),
    Column('Sex', Unicode(150)),
    Column('Ring', Unicode(100)),
    Column('BreedingRing', Unicode(100)),
    Column('ReleaseRing', Unicode(100)),
    Column('ChipCode', Unicode(100)),
    Column('Mark1Color', Unicode(150)),
    Column('Mark1Position', Unicode(150)),
    Column('Mark1Code', Unicode(100)),
    Column('Mark2Color', Unicode(150)),
    Column('Mark2Position', Unicode(150)),
    Column('Mark2Code', Unicode(100)),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('Age', Unicode(150)),
    Column('StaType', String(11, 'French_CI_AS')),
    Column('Sta_ID', Integer),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('DaysSinceFirstStation', Integer, nullable=False),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('FW1', Integer),
    Column('FW2', Integer),
    Column('FA_ID', Integer),
    Column('FA', Unicode(255)),
    Column('Creator', Integer),
    Column('CreationDate', DateTime)
)


t_V_Qry_AllIndivs_FirstStation_LC = Table(
    'V_Qry_AllIndivs_FirstStation_LC', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentIndividualStatus', Unicode(250)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('CurrentPTTModel', Unicode(150)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('Sex', Unicode(150)),
    Column('Ring', Unicode(100)),
    Column('BreedingRing', Unicode(100)),
    Column('ReleaseRing', Unicode(100)),
    Column('ChipCode', Unicode(100)),
    Column('Mark1Color', Unicode(150)),
    Column('Mark1Position', Unicode(150)),
    Column('Mark1Code', Unicode(100)),
    Column('Mark2Color', Unicode(150)),
    Column('Mark2Position', Unicode(150)),
    Column('Mark2Code', Unicode(100)),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('Age', Unicode(150)),
    Column('StaType', String(7, 'French_CI_AS')),
    Column('Sta_ID', Integer),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('DaysSinceFirstStation', Integer, nullable=False),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer)
)


t_V_Qry_AllIndivs_LastStations = Table(
    'V_Qry_AllIndivs_LastStations', metadata,
    Column('Name', Unicode(255)),
    Column('Site_name', Unicode(50)),
    Column('StaName', Unicode(255)),
    Column('label', Unicode(31)),
    Column('Fk_TInd_ID', Integer, nullable=False),
    Column('Frequency', Integer),
    Column('FreqOpti', Integer),
    Column('PTT', Integer),
    Column('id34@TCaracThes_Species_Precision', Unicode(150)),
    Column('species', Unicode(150)),
    Column('NumBagRel', Unicode(100)),
    Column('Breeding_ring_code', Unicode(100)),
    Column('MonitoringStatus@Station', Unicode(1000)),
    Column('SurveyType@station', Unicode(1000)),
    Column('CurrentMonStatus', Unicode(150)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('Origin', Unicode(150)),
    Column('Sex', Unicode(150)),
    Column('Age', Unicode(150)),
    Column('TSta_PK_ID', Integer, nullable=False),
    Column('FieldWorker1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FieldWorker2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NbFieldWorker', Integer),
    Column('FieldActivity_Name', Unicode(255)),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('DATE', DateTime),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('ELE', Integer),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Creation_date', DateTime),
    Column('TSta_FK_TGeo_ID', Integer),
    Column('Site_Idtype', Integer),
    Column('Site_type', Unicode(200)),
    Column('FieldActivity_ID', Integer)
)


t_V_Qry_AllIndivs_LastStations_WithFirstRelCaptData = Table(
    'V_Qry_AllIndivs_LastStations_WithFirstRelCaptData', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('CurrentIndividualStatus', Unicode(250)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('CurrentPTTModel', Unicode(150)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('MonitoringStatus@Station', Unicode(1000)),
    Column('SurveyType@Station', Unicode(1000)),
    Column('freqOpti@Station', Integer),
    Column('Sex', Unicode(150)),
    Column('BreedingRing', Unicode(100)),
    Column('ReleaseRing', Unicode(100)),
    Column('Ring', Unicode(100)),
    Column('ChipCode', Unicode(100)),
    Column('Mark1Color', Unicode(150)),
    Column('Mark1Position', Unicode(150)),
    Column('Mark1Code', Unicode(100)),
    Column('Mark2Color', Unicode(150)),
    Column('Mark2Position', Unicode(150)),
    Column('Mark2Code', Unicode(100)),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('Age', Unicode(150)),
    Column('RelCaptSta_ID', Integer),
    Column('RelCaptStaType', String(11, 'French_CI_AS')),
    Column('RelCaptStaDate', DateTime),
    Column('RelCaptYear', Integer),
    Column('RelCaptRegion', Unicode(255)),
    Column('RelCaptPlace', Unicode(50)),
    Column('RelCaptLAT', Numeric(9, 5)),
    Column('RelCaptLON', Numeric(9, 5)),
    Column('RelCaptMethod', Unicode(250)),
    Column('StaType', String(11, 'French_CI_AS')),
    Column('Sta_ID', Integer),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('DaysSinceFirstStation', Integer),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('FW1', Integer),
    Column('FW2', Integer),
    Column('FA_ID', Integer),
    Column('FA', Unicode(255)),
    Column('Creator', Integer),
    Column('CreationDate', DateTime)
)


t_V_Qry_AllIndivs_Released_FirstStation = Table(
    'V_Qry_AllIndivs_Released_FirstStation', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('CurrentIndividualStatus', Unicode(250)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('CurrentPTTModel', Unicode(150)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('Sex', Unicode(150)),
    Column('BreedindRing', Unicode(100)),
    Column('ReleaseRing', Unicode(100)),
    Column('ChipCode', Unicode(100)),
    Column('Mark1Color', Unicode(150)),
    Column('Mark1Position', Unicode(150)),
    Column('Mark1Code', Unicode(100)),
    Column('Mark2Color', Unicode(150)),
    Column('Mark2Position', Unicode(150)),
    Column('Mark2Code', Unicode(100)),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('WeightGrs', Float(53)),
    Column('Skull', Float(53)),
    Column('Tarso_Metatarsus', Float(53)),
    Column('RelMethod_ID', Integer),
    Column('RelMethod', Unicode(250)),
    Column('RelComments', Unicode(255)),
    Column('StaType', String(7, 'French_CI_AS'), nullable=False),
    Column('Sta_ID', Integer, nullable=False),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('DaysSinceRelease', Integer, nullable=False),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('ELE', Integer),
    Column('Precision', Integer),
    Column('FW1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FW2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FA_ID', Integer),
    Column('FA', Unicode(255)),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CreationDate', DateTime),
    Column('IndivComments', Unicode(100)),
    Column('BiometryComments', String(1000, 'French_CI_AS')),
    Column('BiometryWeight', Float(53)),
    Column('VertebrateIndivComments', Unicode(100)),
    Column('BioStation_ID', Integer)
)


t_V_Qry_AllIndivs_Stations = Table(
    'V_Qry_AllIndivs_Stations', metadata,
    Column('Pr_PK', Integer, nullable=False),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('FW1', Integer),
    Column('FW2', Integer),
    Column('FA_ID', Integer),
    Column('FA', Unicode(255)),
    Column('Creator', Integer),
    Column('CreationDate', DateTime),
    Column('Ind_ID', Integer, nullable=False),
    Column('Taxon', Unicode(150)),
    Column('Origin_ID', Integer),
    Column('Origin', Unicode(150)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('MonitoringStatus@Station', Unicode(1000)),
    Column('SurveyType@Station', Unicode(1000)),
    Column('StaType', String(11, 'French_CI_AS'), nullable=False),
    Column('StaType_ID', Integer, nullable=False),
    Column('Sta_ID', Integer, nullable=False),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('MonitoringStatus@Current', Unicode(150)),
    Column('SurveyType@Current', Unicode(150)),
    Column('IndividualStatus@Current', Unicode(250)),
    Column('freqOpti@Station', Integer)
)


t_V_Qry_AllMicroChipScanningValidatedData = Table(
    'V_Qry_AllMicroChipScanningValidatedData', metadata,
    Column('RFIDModule', String(32, 'French_CI_AS'), nullable=False),
    Column('Site_Name', Unicode(50)),
    Column('begin_date', DateTime, nullable=False),
    Column('end_date', DateTime),
    Column('Ind_Id', Integer, nullable=False),
    Column('ReadingDate', DateTime, nullable=False),
    Column('Taxon', Unicode(150)),
    Column('Origin', Unicode(150)),
    Column('Sex', Unicode(150)),
    Column('Age', Unicode(150)),
    Column('ChipCode', Unicode(100)),
    Column('BreRingCode', Unicode(100)),
    Column('RelCode', Unicode(100)),
    Column('PTT_GSM', Integer),
    Column('VHF', Integer),
    Column('IndStatus', Unicode(250)),
    Column('MonStatus', Unicode(150)),
    Column('SurveyType', Unicode(150)),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('IndComments', Unicode(255))
)


t_V_Qry_ArgosGSM_lastData_withFirstCaptRelData = Table(
    'V_Qry_ArgosGSM_lastData_withFirstCaptRelData', metadata,
    Column('Individual_Obj_PK', Integer, nullable=False),
    Column('PTT', Integer),
    Column('RelCaptTag', Unicode(100)),
    Column('Sex', Unicode(150)),
    Column('Origin', Unicode(150)),
    Column('Monitoring_status', Unicode(150)),
    Column('Survey_type', Unicode(150)),
    Column('speciesId', Integer),
    Column('species', Unicode(150)),
    Column('lastArgosDate', DateTime),
    Column('lastArgosLat', Numeric(9, 5)),
    Column('lastArgosLon', Numeric(9, 5)),
    Column('lastGPSDate', DateTime),
    Column('lastGPSLat', Numeric(9, 5)),
    Column('lastGPSLon', Numeric(9, 5)),
    Column('firstStaType', String(11, 'French_CI_AS')),
    Column('firstStaID', Integer),
    Column('firstStaName', Unicode(255)),
    Column('firstStaDate', DateTime),
    Column('firstStaRegion', Unicode(255)),
    Column('firstStaPlace', Unicode(50)),
    Column('firstStaLAT', Numeric(9, 5)),
    Column('firstStaLON', Numeric(9, 5)),
    Column('firstStaPrecision', Integer),
    Column('firstStaFW1', Integer),
    Column('firstStaFW2', Integer),
    Column('firstStaFA_ID', Integer),
    Column('firstStaFA', Unicode(255)),
    Column('Lat', Numeric(9, 5)),
    Column('Lon', Numeric(9, 5)),
    Column('region', Unicode(255)),
    Column('datediffGPS', Integer),
    Column('datediffArgos', Integer),
    Column('BreRingCode', Unicode(100)),
    Column('Age', Unicode(150)),
    Column('BirthDate', DateTime),
    Column('lastGPSregion', Unicode(255)),
    Column('lastArgosregion', Unicode(255)),
    Column('lastStageom', NullType)
)


t_V_Qry_ArgosGSM_lastData_withFirstCaptRelData_GeoCountry = Table(
    'V_Qry_ArgosGSM_lastData_withFirstCaptRelData_GeoCountry', metadata,
    Column('Individual_Obj_PK', Integer, nullable=False),
    Column('PTT', Integer),
    Column('RelCaptTag', Unicode(100)),
    Column('Sex', Unicode(150)),
    Column('Origin', Unicode(150)),
    Column('Monitoring_status', Unicode(150)),
    Column('Survey_type', Unicode(150)),
    Column('speciesId', Integer),
    Column('species', Unicode(150)),
    Column('lastArgosDate', DateTime),
    Column('lastArgosLat', Numeric(9, 5)),
    Column('lastArgosLon', Numeric(9, 5)),
    Column('lastGPSDate', DateTime),
    Column('lastGPSLat', Numeric(9, 5)),
    Column('lastGPSLon', Numeric(9, 5)),
    Column('firstStaType', String(11, 'French_CI_AS')),
    Column('firstStaID', Integer),
    Column('firstStaName', Unicode(255)),
    Column('firstStaDate', DateTime),
    Column('firstStaRegion', Unicode(255)),
    Column('firstStaPlace', Unicode(50)),
    Column('firstStaLAT', Numeric(9, 5)),
    Column('firstStaLON', Numeric(9, 5)),
    Column('firstStaPrecision', Integer),
    Column('firstStaFW1', Integer),
    Column('firstStaFW2', Integer),
    Column('firstStaFA_ID', Integer),
    Column('firstStaFA', Unicode(255)),
    Column('Lat', Numeric(9, 5)),
    Column('Lon', Numeric(9, 5)),
    Column('region', Unicode(255)),
    Column('datediffGPS', Integer),
    Column('datediffArgos', Integer),
    Column('BreRingCode', Unicode(100)),
    Column('Age', Unicode(150)),
    Column('BirthDate', DateTime),
    Column('lastGPSregion', Unicode(255)),
    Column('lastArgosregion', Unicode(255)),
    Column('lastStageom', NullType),
    Column('country', Unicode(255))
)


t_V_Qry_Argos_AllIndivs_AllStations = Table(
    'V_Qry_Argos_AllIndivs_AllStations', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('PTT', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('MonitoringStatus@Station', Unicode(1000)),
    Column('SurveyType@Station', Unicode(1000)),
    Column('Origin', Unicode(150)),
    Column('Sex', Unicode(150)),
    Column('Age', Unicode(150)),
    Column('RelCaptTag', Unicode(100)),
    Column('BreedingRingCode', Unicode(100)),
    Column('CurrentIndividualStatus', Unicode(250)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('TypeOfData', String(11, 'French_CI_AS'), nullable=False),
    Column('TSta_PK_ID', Integer, nullable=False),
    Column('Name', Unicode(255)),
    Column('FieldWorker1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FieldWorker2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NbFieldWorker', Integer),
    Column('FieldActivity_Name', Unicode(255)),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('DATE', DateTime),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('ELE', Integer),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Creation_date', DateTime),
    Column('FieldActivity_ID', Integer)
)


t_V_Qry_Argos_AllIndivs_LastStations = Table(
    'V_Qry_Argos_AllIndivs_LastStations', metadata,
    Column('Ind_ID', Integer),
    Column('PTT', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('MonitoringStatus@Station', Unicode(1000)),
    Column('SurveyType@Station', Unicode(1000)),
    Column('Origin', Unicode(150)),
    Column('Sex', Unicode(150)),
    Column('Age', Unicode(150)),
    Column('RelCaptTag', Unicode(100)),
    Column('BreedingRingCode', Unicode(100)),
    Column('CurrentIndividualStatus', Unicode(250)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('TypeOfData', String(11, 'French_CI_AS')),
    Column('TSta_PK_ID', Integer, nullable=False),
    Column('FieldWorker1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FieldWorker2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NbFieldWorker', Integer),
    Column('FieldActivity_Name', Unicode(255)),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('DATE', DateTime),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('ELE', Integer),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Creation_date', DateTime),
    Column('FieldActivity_ID', Integer)
)


t_V_Qry_Argos_CurrentMonitoredIndividuals_AllStations = Table(
    'V_Qry_Argos_CurrentMonitoredIndividuals_AllStations', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('PTT', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('MonitoringStatus@Station', Unicode(1000)),
    Column('SurveyType@Station', Unicode(1000)),
    Column('Origin', Unicode(150)),
    Column('Sex', Unicode(150)),
    Column('Age', Unicode(150)),
    Column('RelCaptTag', Unicode(100)),
    Column('BreedingRingCode', Unicode(100)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('TypeOfData', String(11, 'French_CI_AS'), nullable=False),
    Column('TSta_PK_ID', Integer, nullable=False),
    Column('FieldWorker1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FieldWorker2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NbFieldWorker', Integer),
    Column('FieldActivity_Name', Unicode(255)),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('DATE', DateTime),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('ELE', Integer),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Creation_date', DateTime),
    Column('FieldActivity_ID', Integer)
)


t_V_Qry_Argos_DataPerDay_withStatus_60j_90j_365j_xj_AllIndiv_LC = Table(
    'V_Qry_Argos_DataPerDay_withStatus_60j_90j_365j_xj_AllIndiv_LC', metadata,
    Column('ind_id', Integer, nullable=False),
    Column('Age', Unicode(150)),
    Column('currentPTT', Unicode(250), nullable=False),
    Column('Release_Code', Unicode(100)),
    Column('Breeding_Code', Unicode(100)),
    Column('Chip_Code', Unicode(100)),
    Column('Sex', Unicode(150)),
    Column('Origine', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('Birth_Date', DateTime),
    Column('Death_Date', DateTime),
    Column('Ind_Status', Unicode(250)),
    Column('Monitoring_Status', Unicode(150)),
    Column('Survey_Type', Unicode(150)),
    Column('Current_VHF', Integer),
    Column('Current_PTT', Integer),
    Column('VHF_Station', Unicode(250)),
    Column('PTT_Station', Unicode(250)),
    Column('VHF_FirstStation', Unicode(250)),
    Column('PTT_FirstStation', Unicode(250)),
    Column('firstStaType', String(7, 'French_CI_AS')),
    Column('firstStaDate', DateTime),
    Column('firstStaRegion', Unicode(255)),
    Column('FK_TSta_ID', Integer),
    Column('StaType', String(7, 'French_CI_AS')),
    Column('Name', Unicode(255)),
    Column('DATE', DateTime),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('d_xj_PK', Integer),
    Column('d_xj_status', String(15, 'French_CI_AS'), nullable=False),
    Column('d_xj_lastDate', DateTime),
    Column('d_xj_MaxDateDiff', Integer),
    Column('d_xj_dateDiffSinceRel', Integer),
    Column('d_365j_PK', Integer),
    Column('d_365j_status', String(15, 'French_CI_AS')),
    Column('d_365j_lastDate', DateTime),
    Column('d_365j_MaxDateDiff', Integer),
    Column('d_90j_PK', Integer),
    Column('d_90j_status', String(15, 'French_CI_AS')),
    Column('d_90j_lastDate', DateTime),
    Column('d_90j_MaxDateDiff', Integer),
    Column('d_60j_PK', Integer),
    Column('d_60j_status', String(15, 'French_CI_AS')),
    Column('d_60j_lastDate', DateTime),
    Column('d_60j_dateDiffSinceRel', Integer)
)


t_V_Qry_Argos_DataPerDay_withStatus_60j_90j_365j_xj_AllIndividuals = Table(
    'V_Qry_Argos_DataPerDay_withStatus_60j_90j_365j_xj_AllIndividuals', metadata,
    Column('ind_id', Integer, nullable=False),
    Column('Age', Unicode(150)),
    Column('currentPTT', Unicode(250), nullable=False),
    Column('Release_Code', Unicode(100)),
    Column('Breeding_Code', Unicode(100)),
    Column('Chip_Code', Unicode(100)),
    Column('Sex', Unicode(150)),
    Column('Origine', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('Birth_Date', DateTime),
    Column('Death_Date', DateTime),
    Column('Ind_Status', Unicode(250)),
    Column('Monitoring_Status', Unicode(150)),
    Column('Survey_Type', Unicode(150)),
    Column('Current_VHF', Integer),
    Column('Current_PTT', Integer),
    Column('VHF_Station', Unicode(250)),
    Column('PTT_Station', Unicode(250)),
    Column('VHF_FirstStation', Unicode(250)),
    Column('PTT_FirstStation', Unicode(250)),
    Column('firstStaType', String(11, 'French_CI_AS')),
    Column('firstStaDate', DateTime),
    Column('firstStaRegion', Unicode(255)),
    Column('FK_TSta_ID', Integer),
    Column('StaType', String(11, 'French_CI_AS')),
    Column('Name', Unicode(255)),
    Column('DATE', DateTime),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('d_xj_PK', Integer),
    Column('d_xj_status', String(15, 'French_CI_AS'), nullable=False),
    Column('d_xj_lastDate', DateTime),
    Column('d_xj_MaxDateDiff', Integer),
    Column('d_xj_dateDiffSinceRel', Integer),
    Column('d_365j_PK', Integer),
    Column('d_365j_status', String(15, 'French_CI_AS')),
    Column('d_365j_lastDate', DateTime),
    Column('d_365j_MaxDateDiff', Integer),
    Column('d_90j_PK', Integer),
    Column('d_90j_status', String(15, 'French_CI_AS')),
    Column('d_90j_lastDate', DateTime),
    Column('d_90j_MaxDateDiff', Integer),
    Column('d_60j_PK', Integer),
    Column('d_60j_status', String(15, 'French_CI_AS')),
    Column('d_60j_lastDate', DateTime),
    Column('d_60j_dateDiffSinceRel', Integer)
)


t_V_Qry_Argos_DataPerDay_withStatus_60j_90j_365j_xj_CurrentIndiv = Table(
    'V_Qry_Argos_DataPerDay_withStatus_60j_90j_365j_xj_CurrentIndiv', metadata,
    Column('ind_id', Integer, nullable=False),
    Column('Age', Unicode(150)),
    Column('currentPTT', Integer),
    Column('Release_Code', Unicode(100)),
    Column('Breeding_Code', Unicode(100)),
    Column('Chip_Code', Unicode(100)),
    Column('Sex', Unicode(150)),
    Column('Origine', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('Birth_Date', DateTime),
    Column('Death_Date', DateTime),
    Column('Ind_Status', Unicode(250)),
    Column('Monitoring_Status', Unicode(150)),
    Column('Survey_Type', Unicode(150)),
    Column('Current_VHF', Integer),
    Column('Current_PTT', Integer),
    Column('VHF_Station', Unicode(250)),
    Column('PTT_Station', Unicode(250)),
    Column('firstStaType', String(11, 'French_CI_AS')),
    Column('firstStaDate', DateTime),
    Column('firstStaRegion', Unicode(255)),
    Column('FK_TSta_ID', Integer),
    Column('StaType', String(11, 'French_CI_AS')),
    Column('Name', Unicode(255)),
    Column('DATE', DateTime),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('d_xj_PK', Integer),
    Column('d_xj_status', String(15, 'French_CI_AS'), nullable=False),
    Column('d_xj_lastDate', DateTime),
    Column('d_xj_MaxDateDiff', Integer),
    Column('d_xj_dateDiffSinceRel', Integer),
    Column('d_365j_PK', Integer),
    Column('d_365j_status', String(15, 'French_CI_AS')),
    Column('d_365j_lastDate', DateTime),
    Column('d_365j_MaxDateDiff', Integer),
    Column('d_90j_PK', Integer),
    Column('d_90j_status', String(15, 'French_CI_AS')),
    Column('d_90j_lastDate', DateTime),
    Column('d_90j_MaxDateDiff', Integer),
    Column('d_60j_PK', Integer),
    Column('d_60j_status', String(15, 'French_CI_AS')),
    Column('d_60j_lastDate', DateTime),
    Column('d_60j_dateDiffSinceRel', Integer)
)


t_V_Qry_Chiro_capture = Table(
    'V_Qry_Chiro_capture', metadata,
    Column('Vernacular_name', Unicode(255)),
    Column('Latin_name', Unicode),
    Column('Dead', BIT, nullable=False),
    Column('Number', String(1, 'French_CI_AS'), nullable=False),
    Column('Hour', DateTime),
    Column('Ind_Id', Unicode(50)),
    Column('Age', Unicode(255)),
    Column('Sex', Unicode(255)),
    Column('Sampled', BIT, nullable=False),
    Column('Picture', BIT, nullable=False),
    Column('Recatch', BIT, nullable=False),
    Column('Recorded', BIT, nullable=False),
    Column('Comments', Unicode(255)),
    Column('FA', Float(53)),
    Column('Tib', Float(53)),
    Column('D3', Float(53)),
    Column('D3_1', Float(53)),
    Column('D3_2', Float(53)),
    Column('D3_3', Float(53)),
    Column('D4', Float(53)),
    Column('D4_1', Float(53)),
    Column('D4_2', Float(53)),
    Column('D5', Float(53)),
    Column('D5_1', Float(53)),
    Column('D5_2', Float(53)),
    Column('CM3', Float(53)),
    Column('D1', Float(53)),
    Column('Claw_D1', Float(53)),
    Column('tragus_Lenght', Float(53)),
    Column('tragus_Width', Float(53)),
    Column('Weight', Float(53)),
    Column('CommentsBiometry', Unicode(255)),
    Column('Reproductive_Status_male', Unicode(255)),
    Column('Reproductive_Status_female', Unicode(255)),
    Column('Maturity_Female', Unicode(255)),
    Column('CommentsPhysiology', Unicode(255)),
    Column('TSta_PK_ID', Integer, nullable=False),
    Column('FieldWorker1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FieldWorker2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NbFieldWorker', Integer),
    Column('FieldActivity_Name', Unicode(255)),
    Column('Name', Unicode(255)),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('DATE', DateTime),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('ELE', Integer),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Creation_date', DateTime),
    Column('TSta_FK_TGeo_ID', Integer),
    Column('Site_name', Unicode(50)),
    Column('Site_idType', Integer),
    Column('Site_type', Unicode(200)),
    Column('FieldActivity_ID', Integer),
    Column('NumEnregistrement', Integer, nullable=False)
)


t_V_Qry_Chiro_detection = Table(
    'V_Qry_Chiro_detection', metadata,
    Column('Vernacular_name', Unicode(255)),
    Column('Latin_name', Unicode),
    Column('Ind_Id', Unicode(50)),
    Column('Number', Integer),
    Column('Time', DateTime),
    Column('Recorded', BIT, nullable=False),
    Column('Comments', Unicode(255)),
    Column('Record_type', Unicode(255)),
    Column('File_name', Unicode(255)),
    Column('Call_type', Unicode(255)),
    Column('Flutter_0_min', Float(53)),
    Column('Flutter_0_max', Float(53)),
    Column('Activity', Unicode(255)),
    Column('TSta_PK_ID', Integer, nullable=False),
    Column('FieldWorker1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FieldWorker2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NbFieldWorker', Integer),
    Column('FieldActivity_Name', Unicode(255)),
    Column('Name', Unicode(255)),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('DATE', DateTime),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('ELE', Integer),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Creation_date', DateTime),
    Column('TSta_FK_TGeo_ID', Integer),
    Column('Site_name', Unicode(50)),
    Column('Site_idType', Integer),
    Column('Site_type', Unicode(200)),
    Column('FieldActivity_ID', Integer),
    Column('NumEnregistrement', Integer, nullable=False)
)


t_V_Qry_DeathStation_AllIndivs_FirstSta_Equip_Data = Table(
    'V_Qry_DeathStation_AllIndivs_FirstSta_Equip_Data', metadata,
    Column('Ind_Id', Integer),
    Column('BreedRing', Unicode(100)),
    Column('Generation', Unicode(4000)),
    Column('ChipCode', Unicode(100)),
    Column('RelRing', Unicode(100)),
    Column('Origin', Unicode(150)),
    Column('Sex', Unicode(150)),
    Column('FirstStaPTT', Unicode(250)),
    Column('FirstStaVHF', Unicode(250)),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('DeathStaPTT', Unicode(250)),
    Column('DeathStaVHF', Unicode(250)),
    Column('DeathStaID', Integer, nullable=False),
    Column('DeathStaName', Unicode(255)),
    Column('DeathStaDate', DateTime),
    Column('DeathStaLAT', Numeric(9, 5)),
    Column('DeathStaLON', Numeric(9, 5)),
    Column('DeathStaPrecision', Integer),
    Column('DeathStaRegion', Unicode(255)),
    Column('DeathStaPlace', Unicode(50)),
    Column('Taxon', Unicode(255)),
    Column('DeathReason', Unicode(250)),
    Column('DeathTime', Unicode(250)),
    Column('Sure', BIT, nullable=False),
    Column('Sampled', BIT, nullable=False),
    Column('DeathComments', Unicode(500)),
    Column('FirstStaID', Integer),
    Column('FirstStaName', Unicode(255)),
    Column('FirstStaDate', DateTime),
    Column('FirstStaRegion', Unicode(255)),
    Column('FirstStaLAT', Numeric(9, 5)),
    Column('FirstStaLON', Numeric(9, 5)),
    Column('DeathPK', Integer, nullable=False)
)


t_V_Qry_Death_AllIndivs_AllStations = Table(
    'V_Qry_Death_AllIndivs_AllStations', metadata,
    Column('FK_TInd_ID', Integer),
    Column('Origin', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('Sex', Unicode(150)),
    Column('Death_date', DateTime),
    Column('TSta_PK_ID', Integer, nullable=False),
    Column('Field_activity', Unicode(255)),
    Column('DATE', DateTime),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('Reason_of_death', Unicode(250)),
    Column('Sure', BIT, nullable=False),
    Column('Rest', Unicode(250)),
    Column('Death_time', Unicode(250)),
    Column('Comments', Unicode(500))
)


t_V_Qry_Death_AllIndivs_WithFirstStation_DeathStationEquipment = Table(
    'V_Qry_Death_AllIndivs_WithFirstStation_DeathStationEquipment', metadata,
    Column('deathDate', DateTime),
    Column('Individual_Obj_PK', Integer, nullable=False),
    Column('id2@Thes_Age', Integer),
    Column('id2@Thes_Age_Precision', Unicode(150)),
    Column('id3@TCaracThes_Transmitter_Shape', Integer),
    Column('id3@TCaracThes_Transmitter_Shape_Precision', Unicode(150)),
    Column('id4@TCaracThes_Transmitter_Model', Integer),
    Column('id4@TCaracThes_Transmitter_Model_Precision', Unicode(150)),
    Column('id5@TCarac_Transmitter_Frequency', Integer),
    Column('id6@TCarac_Transmitter_Serial_Number', Unicode(100)),
    Column('id7@TCaracThes_Release_Ring_Position', Integer),
    Column('id7@TCaracThes_Release_Ring_Position_Precision', Unicode(150)),
    Column('id8@TCaracThes_Release_Ring_Color', Integer),
    Column('id8@TCaracThes_Release_Ring_Color_Precision', Unicode(150)),
    Column('id9@TCarac_Release_Ring_Code', Unicode(100)),
    Column('id10@TCaracThes_Breeding_Ring_Position', Integer),
    Column('id10@TCaracThes_Breeding_Ring_Position_Precision', Unicode(150)),
    Column('id11@TCaracThes_Breeding_Ring_Color', Integer),
    Column('id11@TCaracThes_Breeding_Ring_Color_Precision', Unicode(150)),
    Column('id12@TCarac_Breeding_Ring_Code', Unicode(100)),
    Column('id13@TCarac_Chip_Code', Unicode(100)),
    Column('id14@TCaracThes_Mark_Color_1', Integer),
    Column('id14@TCaracThes_Mark_Color_1_Precision', Unicode(150)),
    Column('id15@TCaracThes_Mark_Position_1', Integer),
    Column('id15@TCaracThes_Mark_Position_1_Precision', Unicode(150)),
    Column('id16@TCaracThes_Mark_Color_2', Integer),
    Column('id16@TCaracThes_Mark_Color_2_Precision', Unicode(150)),
    Column('id17@TCaracThes_Mark_Position_2', Integer),
    Column('id17@TCaracThes_Mark_Position_2_Precision', Unicode(150)),
    Column('id19@TCarac_PTT', Integer),
    Column('id20@TCaracThes_PTT_manufacturer', Integer),
    Column('id20@TCaracThes_PTT_manufacturer_Precision', Unicode(150)),
    Column('id22@TCaracThes_PTT_model', Integer),
    Column('id22@TCaracThes_PTT_model_Precision', Unicode(150)),
    Column('id30@TCaracThes_Sex', Integer),
    Column('id30@TCaracThes_Sex_Precision', Unicode(150)),
    Column('id33@Thes_Origin', Integer),
    Column('id33@Thes_Origin_Precision', Unicode(150)),
    Column('id34@TCaracThes_Species', Integer),
    Column('id34@TCaracThes_Species_Precision', Unicode(150)),
    Column('id35@Birth_date', DateTime),
    Column('id36@Death_date', DateTime),
    Column('id37@Comments', Unicode(255)),
    Column('id55@TCarac_Mark_code_1', Unicode(100)),
    Column('id56@TCarac_Mark_code_2', Unicode(100)),
    Column('id59@TCaracThes_Individual_Status', Unicode(250)),
    Column('id60@TCaracThes_Monitoring_Status', Integer),
    Column('id60@TCaracThes_Monitoring_Status_Precision', Unicode(150)),
    Column('id61@TCaracThes_Survey_type', Integer),
    Column('id61@TCaracThes_Survey_type_Precision', Unicode(150)),
    Column('PK', Integer),
    Column('FK_TSta_ID', Integer),
    Column('FK_TInd_ID', Integer),
    Column('Id_Remains', Integer),
    Column('Name_Remains', Unicode(250)),
    Column('Id_Death_Time', Integer),
    Column('Name_Death_Time', Unicode(250)),
    Column('Id_Death_Reason', Integer),
    Column('Name_Death_Reason', Unicode(250)),
    Column('Identification_criteria', Unicode(500)),
    Column('Sure_reason', BIT),
    Column('Identification_type', Unicode(10)),
    Column('Comments', Unicode(500)),
    Column('Name_Taxon', Unicode(255)),
    Column('Id_Taxon', Integer),
    Column('Sampled', BIT),
    Column('TSta_PK_ID', Integer),
    Column('FieldWorker1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FieldWorker2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NbFieldWorker', Integer),
    Column('FieldActivity_Name', Unicode(255)),
    Column('Name', Unicode(255)),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('DATE', DateTime),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('ELE', Integer),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Creation_date', DateTime),
    Column('TSta_FK_TGeo_ID', Integer),
    Column('Site_name', Unicode(50)),
    Column('Site_idType', Integer),
    Column('Site_type', Unicode(200)),
    Column('FieldActivity_ID', Integer),
    Column('firstStaDate', DateTime),
    Column('firststaregion', Unicode(255)),
    Column('VHF@Station', Unicode(250)),
    Column('PTT@Station', Unicode(250))
)


t_V_Qry_Display_AllStations_with_males_data = Table(
    'V_Qry_Display_AllStations_with_males_data', metadata,
    Column('TSta_PK_ID', Integer, nullable=False),
    Column('FieldWorker1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FieldWorker2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NbFieldWorker', Integer),
    Column('FieldActivity_Name', Unicode(255)),
    Column('Name', Unicode(255)),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('DATE', DateTime),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('ELE', Integer),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Creation_date', DateTime),
    Column('TSta_FK_TGeo_ID', Integer),
    Column('Site_name', Unicode(50)),
    Column('Site_idType', Integer),
    Column('Site_type', Unicode(200)),
    Column('FieldActivity_ID', Integer),
    Column('Individual_ID', Integer),
    Column('Frequency', Integer),
    Column('Transmitter_shape', Unicode(150)),
    Column('TransmitterModel', Unicode(150)),
    Column('Transmitter_serial_number', Unicode(100)),
    Column('PTT', Integer),
    Column('PTT_manufacturer', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('Age', Unicode(150)),
    Column('Release_ring_code', Unicode(100)),
    Column('Chip_code', Unicode(100)),
    Column('Breeding_ring_code', Unicode(100)),
    Column('Sex', Unicode(150)),
    Column('Origin', Unicode(150)),
    Column('Birthdate', DateTime),
    Column('Death_date', DateTime),
    Column('Individual_behaviour', Unicode(250)),
    Column('Individual_id_behaviour', Integer),
    Column('Identification_criteria', Unicode(500)),
    Column('Measured_Distance', Numeric(9, 2)),
    Column('Transmitter_Type', String(15, 'French_CI_AS')),
    Column('Transmitter_Model', String(14, 'French_CI_AS')),
    Column('TrxPrsce', String(7, 'French_CI_AS')),
    Column('RelRingPosition', String(7, 'French_CI_AS')),
    Column('BreRingPosition', String(7, 'French_CI_AS')),
    Column('RingPsce', String(7, 'French_CI_AS')),
    Column('RelRing Color', String(5, 'French_CI_AS')),
    Column('BreRing Color', String(5, 'French_CI_AS')),
    Column('PK_VIndiv', Integer, nullable=False)
)


t_V_Qry_Houbara_AllStations = Table(
    'V_Qry_Houbara_AllStations', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('CurrentPTTModel', Unicode(150)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('Sex', Unicode(150)),
    Column('BreedingRing', Unicode(100)),
    Column('ReleaseRing', Unicode(100)),
    Column('ChipCode', Unicode(100)),
    Column('Mark1Color', Unicode(150)),
    Column('Mark1Position', Unicode(150)),
    Column('Mark1Code', Integer),
    Column('Mark2Color', Unicode(150)),
    Column('Mark2Position', Unicode(150)),
    Column('Mark2Code', Integer),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('StaType', String(11, 'French_CI_AS'), nullable=False),
    Column('Sta_ID', Integer, nullable=False),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('FW1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FW2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FA_ID', Integer),
    Column('FA', Unicode(255)),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CreationDate', DateTime)
)


t_V_Qry_Houbara_Displaying_male_survey = Table(
    'V_Qry_Houbara_Displaying_male_survey', metadata,
    Column('Site_name', Unicode(50)),
    Column('MS_LAT', Numeric(9, 5)),
    Column('MS_LON', Numeric(9, 5)),
    Column('ObsStaID', Integer, nullable=False),
    Column('true_obs_point', Unicode(255)),
    Column('ObsLat', Numeric(9, 5)),
    Column('ObsLon', Numeric(9, 5)),
    Column('DATE', DateTime),
    Column('FW1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NbFW', Integer),
    Column('ObsFA', Unicode(255)),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('DisStaID', Integer),
    Column('DisName', Unicode(255)),
    Column('DisLAT', Numeric(9, 5)),
    Column('DisLON', Numeric(9, 5)),
    Column('DisDate', DateTime),
    Column('DisFA', Unicode(255)),
    Column('Measured_Distance', Numeric(9, 2)),
    Column('observation_time', DateTime),
    Column('Name_Behaviour', Unicode(250))
)


t_V_Qry_Houbara_FirstULastStation = Table(
    'V_Qry_Houbara_FirstULastStation', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentIndividualStatus', Unicode(250)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('CurrentPTTModel', Unicode(150)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('Sex', Unicode(150)),
    Column('BreedingRing', Unicode(100)),
    Column('ReleaseRing', Unicode(100)),
    Column('ChipCode', Unicode(100)),
    Column('Mark1Color', Unicode(150)),
    Column('Mark1Position', Unicode(150)),
    Column('Mark1Code', Unicode(100)),
    Column('Mark2Color', Unicode(150)),
    Column('Mark2Position', Unicode(150)),
    Column('Mark2Code', Unicode(100)),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('StaType', String(11, 'French_CI_AS')),
    Column('Sta_ID', Integer),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('DaysSinceFirstStation', Integer),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('FW1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FW2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FA_ID', Integer),
    Column('FA', Unicode(255)),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CreationDate', DateTime)
)


t_V_Qry_Hunting_bag_first_station = Table(
    'V_Qry_Hunting_bag_first_station', metadata,
    Column('Ind_Id', Integer),
    Column('BreedRing', Unicode(100)),
    Column('Generation', Unicode(4000)),
    Column('ChipCode', Unicode(100)),
    Column('RelRing', Unicode(100)),
    Column('Origin', Unicode(150)),
    Column('Sex', Unicode(150)),
    Column('FirstStaPTT', Unicode(250)),
    Column('FirstStaVHF', Unicode(250)),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('DeathStaPTT', Unicode(250)),
    Column('DeathStaVHF', Unicode(250)),
    Column('DeathStaID', Integer, nullable=False),
    Column('DeathStaName', Unicode(255)),
    Column('DeathStaDate', DateTime),
    Column('DeathStaLAT', Numeric(9, 5)),
    Column('DeathStaLON', Numeric(9, 5)),
    Column('DeathStaPrecision', Integer),
    Column('DeathStaRegion', Unicode(255)),
    Column('DeathStaPlace', Unicode(50)),
    Column('Taxon', Unicode(255)),
    Column('DeathReason', Unicode(250)),
    Column('DeathTime', Unicode(250)),
    Column('Sure', BIT, nullable=False),
    Column('Sampled', BIT, nullable=False),
    Column('DeathComments', Unicode(500)),
    Column('FirstStaID', Integer),
    Column('FirstStaName', Unicode(255)),
    Column('FirstStaDate', DateTime),
    Column('FirstStaLAT', Numeric(9, 5)),
    Column('FirstStaLON', Numeric(9, 5)),
    Column('DeathPK', Integer, nullable=False)
)


t_V_Qry_Invalid_Individuals_SexORAge = Table(
    'V_Qry_Invalid_Individuals_SexORAge', metadata,
    Column('Individual_Obj_Pk', Integer, nullable=False),
    Column('Frequency', Integer),
    Column('NumBagRel', Unicode(100)),
    Column('Age', Unicode(150)),
    Column('Sex', Unicode(150)),
    Column('Site_type', Unicode(200)),
    Column('isError', Integer, nullable=False)
)


t_V_Qry_MonitoredSites = Table(
    'V_Qry_MonitoredSites', metadata,
    Column('Name', Unicode(4000)),
    Column('Monitored_site', Unicode(50)),
    Column('IdType', Integer),
    Column('Type', Unicode(200)),
    Column('Date', DateTime),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('ELE', Float(53)),
    Column('TGeo_pk_id', Integer, nullable=False),
    Column('Active', BIT, nullable=False)
)


t_V_Qry_Nest_AllStations_with_relatedMother_data = Table(
    'V_Qry_Nest_AllStations_with_relatedMother_data', metadata,
    Column('Site_name', Unicode(50)),
    Column('TSta_PK_ID', Integer, nullable=False),
    Column('Name', Unicode(255)),
    Column('FieldWorker1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FieldWorker2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('DATE', DateTime),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Fiel_activity', Unicode(255)),
    Column('Name_Taxon', Unicode(255)),
    Column('Id_Clutch_Description', Integer),
    Column('Name_Clutch_Description', Unicode(250)),
    Column('ID_Clutch_Size', Integer),
    Column('Name_Clutch_Size', Unicode(250)),
    Column('Dummy_egg', BIT, nullable=False),
    Column('Nb_Item', Integer),
    Column('NB_newborn_alive', Integer),
    Column('Nb_newborn_dead', Integer),
    Column('TotNbNewborn', Integer),
    Column('Individual_Obj_PK', Integer),
    Column('CurrentIndividualStatus', Unicode(250)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('Age', Unicode(150)),
    Column('Origin', Unicode(150)),
    Column('Frequency', Integer),
    Column('vhf@station', Unicode(250)),
    Column('Transmitter_shape', Unicode(150)),
    Column('Transmitter_model', Unicode(150)),
    Column('Serial_number', Unicode(100)),
    Column('PTT', Integer),
    Column('PTT@station', Unicode(250)),
    Column('PTT_manufacturer', Unicode(150)),
    Column('PTT_model', Unicode(150)),
    Column('Sex', Unicode(150)),
    Column('Release_ring_code', Unicode(100)),
    Column('Breeding_ring_code', Unicode(100)),
    Column('Chip_code', Unicode(100)),
    Column('Birth_date', DateTime),
    Column('Death_date', DateTime),
    Column('Comments', Unicode(255)),
    Column('FK_TIND_ID', Integer),
    Column('Identification criteria', Unicode(500)),
    Column('Transmitter_type', String(15, 'French_CI_AS')),
    Column('TransmitterShape entered', String(1, 'French_CI_AS')),
    Column('TransmitterModel entered', String(1, 'French_CI_AS')),
    Column('Sex entered', String(6, 'French_CI_AS')),
    Column('RelRingPosition', String(7, 'French_CI_AS')),
    Column('BreRingPosition', String(7, 'French_CI_AS')),
    Column('Chip', String(2, 'French_CI_AS')),
    Column('RingPosition entered', String(1, 'French_CI_AS')),
    Column('RelRing Color', String(5, 'French_CI_AS')),
    Column('BreRing Color', String(5, 'French_CI_AS')),
    Column('RingColor entered', String(1, 'French_CI_AS')),
    Column('Species', String(29, 'French_CI_AS')),
    Column('Species entered', String(1, 'French_CI_AS')),
    Column('SensorAction', Unicode(250)),
    Column('SensorType', Unicode(250))
)


t_V_Qry_Nest_Schedule = Table(
    'V_Qry_Nest_Schedule', metadata,
    Column('MS_ID', Integer),
    Column('Site_name', Unicode(50)),
    Column('Place', Unicode(50)),
    Column('Region', Unicode(255)),
    Column('MinDate', DateTime),
    Column('LastVisit', DateTime),
    Column('LastObs', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('LastStaID', Integer, nullable=False),
    Column('MaxItem', Integer),
    Column('LastClutchDesc', Unicode(250)),
    Column('LastClutchSize', Unicode(250)),
    Column('CurrentNestStatus', String(8, 'French_CI_AS'), nullable=False),
    Column('Site_type', Unicode(200)),
    Column('name_action_type', Unicode(250)),
    Column('name_sensor_type', Unicode(250)),
    Column('MinEclDate', String(10, 'French_CI_AS')),
    Column('MaxEclDate', String(10, 'French_CI_AS')),
    Column('NextVisit', DateTime),
    Column('Ind_Id', Integer),
    Column('PTTGSM_VHF', Unicode(250)),
    Column('Ring_Chip_Code', Unicode(100)),
    Column('trx', String(15, 'French_CI_AS')),
    Column('Ring', String(16, 'French_CI_AS')),
    Column('Chip', String(2, 'French_CI_AS'))
)


t_V_Qry_Nest_Schedule_MonitoredNest = Table(
    'V_Qry_Nest_Schedule_MonitoredNest', metadata,
    Column('TSta_PK_ID', Integer),
    Column('FieldWorker1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FieldWorker2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NbFieldWorker', Integer),
    Column('FieldActivity_Name', Unicode(255)),
    Column('Name', Unicode(255)),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('DATE', DateTime),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('ELE', Integer),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Creation_date', DateTime),
    Column('TSta_FK_TGeo_ID', Integer),
    Column('Site_name', Unicode(50)),
    Column('Site_idType', Integer),
    Column('Site_type', Unicode(200)),
    Column('FieldActivity_ID', Integer),
    Column('Nb_Egg', Integer),
    Column('FK_TIND_ID', Integer),
    Column('id19@TCarac_PTT', Integer),
    Column('id5@TCarac_Transmitter_Frequency', Integer),
    Column('id33@Thes_Origin_Precision', Unicode(150)),
    Column('id13@TCarac_Chip_Code', Unicode(100)),
    Column('id9@TCarac_Release_Ring_Code', Unicode(100)),
    Column('HatchingDate', DateTime),
    Column('NextVisiteDate', DateTime),
    Column('CASNextVisiteDate', String(17, 'French_CI_AS'))
)


t_V_Qry_Nest_TheoricalNest_AllYear = Table(
    'V_Qry_Nest_TheoricalNest_AllYear', metadata,
    Column('TSta_FK_TGeo_ID', Integer, nullable=False),
    Column('Name', Unicode(4000)),
    Column('Monitored_site', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('Lon', Numeric(9, 5)),
    Column('ELE', Float(53)),
    Column('DATE', DateTime),
    Column('Precision', Integer),
    Column('site_Type', Unicode(200)),
    Column('site_IdType', Unicode(200)),
    Column('label', Unicode(50)),
    Column('Site_name', Unicode(50)),
    Column('NbFieldworker', Integer),
    Column('Fieldworker1', Integer),
    Column('Fieldworker2', Integer),
    Column('FieldActivity_Name', Integer)
)


t_V_Qry_Plant_Inventory = Table(
    'V_Qry_Plant_Inventory', metadata,
    Column('family', Unicode(255)),
    Column('Taxon', String(255, 'French_CI_AS')),
    Column('ID_Station', Integer, nullable=False),
    Column('Name_Station', Unicode(255)),
    Column('DATE', DateTime),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('ELE', Integer),
    Column('FieldWorker1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FieldWorker2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Protocol', Unicode(255)),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('sampled', BIT, nullable=False),
    Column('Name_Milieu', Unicode(500)),
    Column('Name_Habitat2', Unicode(500)),
    Column('Identity_sure', BIT, nullable=False),
    Column('Comments', Unicode(255)),
    Column('Cultivated', BIT, nullable=False)
)


t_V_Qry_Plant_Phytosociology = Table(
    'V_Qry_Plant_Phytosociology', metadata,
    Column('Station', Unicode(255)),
    Column('DATE', DateTime),
    Column('Annee', Integer),
    Column('family', Unicode(255)),
    Column('Name_Taxon', Unicode, nullable=False),
    Column('A-D', Unicode(50)),
    Column('Soc', Unicode(25)),
    Column('Vegetation_cover', Float(53)),
    Column('FW1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FW2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FieldActivity_Name', Unicode(255)),
    Column('NbFieldWorker', Integer),
    Column('FieldActivity_ID', Integer),
    Column('Name', Unicode(255)),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('ELE', Integer),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Creation_date', DateTime),
    Column('TSta_FK_TGeo_ID', Integer),
    Column('Site_name', Unicode(50)),
    Column('Site_idType', Integer),
    Column('Site_type', Unicode(200))
)


t_V_Qry_Plant_Transects = Table(
    'V_Qry_Plant_Transects', metadata,
    Column('TSta_PK_ID', Integer, nullable=False),
    Column('Station', Unicode(255)),
    Column('family', Unicode(255)),
    Column('Id_Taxon', Integer, nullable=False),
    Column('Taxon', Unicode(1000), nullable=False),
    Column('nb_contact', Integer),
    Column('Nb_Touch', Integer),
    Column('DATE', DateTime),
    Column('Annee', Integer),
    Column('Num_Transect', Integer),
    Column('Nb_transect', Integer),
    Column('FieldWorker1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FieldWorker2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NbFieldWorker', Integer),
    Column('FieldActivity_ID', Integer),
    Column('FieldActivity_Name', Unicode(255)),
    Column('Name', Unicode(255)),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('ELE', Integer),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Creation_date', DateTime),
    Column('TSta_FK_TGeo_ID', Integer),
    Column('Site_name', Unicode(50)),
    Column('Site_idType', Integer),
    Column('Site_type', Unicode(200)),
    Column('Observer', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Assistant', String(201, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_V_Qry_Plant_family = Table(
    'V_Qry_Plant_family', metadata,
    Column('ID', Integer, nullable=False),
    Column('taxon', Unicode(255)),
    Column('Hierarchy', Unicode(15)),
    Column('familyID', Integer, nullable=False),
    Column('family', Unicode(255))
)


t_V_Qry_RFID_PoseRemove = Table(
    'V_Qry_RFID_PoseRemove', metadata,
    Column('RFIDModule', String(32, 'French_CI_AS'), nullable=False),
    Column('Site_Name', Unicode(50)),
    Column('begin_date', DateTime, nullable=False),
    Column('end_date', DateTime),
    Column('lat', Numeric(9, 5), nullable=False),
    Column('lon', Numeric(9, 5), nullable=False),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('creation_date', DateTime)
)


t_V_Qry_Release_FirstLastDeathStationData = Table(
    'V_Qry_Release_FirstLastDeathStationData', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('CurrentIndividualStatus', Unicode(250)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('Sex', Unicode(150)),
    Column('ChipCode', Unicode(100)),
    Column('BreedingRing', Unicode(100)),
    Column('DeathDate', DateTime),
    Column('VHFRelease', Unicode(250)),
    Column('PTTRelease', Unicode(250)),
    Column('RelStaName', Unicode(255)),
    Column('RelStaID', Integer),
    Column('RelStaDate', DateTime),
    Column('RelLat', Numeric(9, 5)),
    Column('RelLon', Numeric(9, 5)),
    Column('RelRegion', Unicode(255)),
    Column('LastStaName', Unicode(255)),
    Column('LastStaId', Integer, nullable=False),
    Column('LastStaDate', DateTime),
    Column('LastStaLat', Numeric(9, 5)),
    Column('LastStaLon', Numeric(9, 5)),
    Column('LastStaType', String(11, 'French_CI_AS'), nullable=False),
    Column('LastStaRegion', Unicode(255)),
    Column('LastStaFA', Unicode(255)),
    Column('DeathStaName', Unicode(255)),
    Column('DeathStaId', Integer),
    Column('DeathStaDate', DateTime),
    Column('DeathStaLat', Numeric(9, 5)),
    Column('DeathStaLon', Numeric(9, 5)),
    Column('DeathRegion', Unicode(255)),
    Column('Name_Death_Reason', Unicode(250)),
    Column('Sure_reason', BIT),
    Column('Comments', Unicode(500))
)


t_V_Qry_Released_AllStations = Table(
    'V_Qry_Released_AllStations', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('CurrentPTTModel', Unicode(150)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('Sex', Unicode(150)),
    Column('ReleaseRing', Unicode(100)),
    Column('ChipCode', Unicode(100)),
    Column('Mark1Color', Unicode(150)),
    Column('Mark1Position', Unicode(150)),
    Column('Mark1Code', Unicode(100)),
    Column('Mark2Color', Unicode(150)),
    Column('Mark2Position', Unicode(150)),
    Column('Mark2Code', Unicode(100)),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('RelMethod_ID', Integer),
    Column('RelMethod', Unicode(250)),
    Column('RelSta_ID', Integer),
    Column('RelStaName', Unicode(255)),
    Column('RelStaDate', DateTime),
    Column('RelRegion', Unicode(255)),
    Column('RelPlace', Unicode(50)),
    Column('StaType', String(11, 'French_CI_AS'), nullable=False),
    Column('Sta_ID', Integer, nullable=False),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('DaysSinceRelease', Integer),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('FW1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FW2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FA_ID', Integer),
    Column('FA', Unicode(255)),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CreationDate', DateTime)
)


t_V_Qry_Released_FirstStation = Table(
    'V_Qry_Released_FirstStation', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('CurrentIndividualStatus', Unicode(250)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('CurrentPTTModel', Unicode(150)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('Sex', Unicode(150)),
    Column('BreedingRing', Unicode(100)),
    Column('ReleaseRing', Unicode(100)),
    Column('ChipCode', Unicode(100)),
    Column('Mark1Color', Unicode(150)),
    Column('Mark1Position', Unicode(150)),
    Column('Mark1Code', Unicode(100)),
    Column('Mark2Color', Unicode(150)),
    Column('Mark2Position', Unicode(150)),
    Column('Mark2Code', Unicode(100)),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('WeightGrs', Float(53)),
    Column('Skull', Float(53)),
    Column('Tarso_Metatarsus', Float(53)),
    Column('RelMethod_ID', Integer),
    Column('RelMethod', Unicode(250)),
    Column('RelComments', Unicode(255)),
    Column('StaType', String(7, 'French_CI_AS'), nullable=False),
    Column('Sta_ID', Integer),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('DaysSinceRelease', Integer, nullable=False),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('FW1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FW2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FA_ID', Integer),
    Column('FA', Unicode(255)),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CreationDate', DateTime),
    Column('IndivComments', Unicode(100)),
    Column('BiometryComments', String(1000, 'French_CI_AS')),
    Column('VertebrateIndivComments', Unicode(100)),
    Column('BioStation_ID', Integer)
)


t_V_Qry_Released_FirstULastStation = Table(
    'V_Qry_Released_FirstULastStation', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('CurrentPTTModel', Unicode(150)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('Sex', Unicode(150)),
    Column('BreedingRing', Unicode(100)),
    Column('ReleaseRing', Unicode(100)),
    Column('ChipCode', Unicode(100)),
    Column('Mark1Color', Unicode(150)),
    Column('Mark1Position', Unicode(150)),
    Column('Mark1Code', Unicode(100)),
    Column('Mark2Color', Unicode(150)),
    Column('Mark2Position', Unicode(150)),
    Column('Mark2Code', Unicode(100)),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('RelMethod_ID', Integer),
    Column('RelMethod', Unicode(250)),
    Column('StaType', String(11, 'French_CI_AS')),
    Column('Sta_ID', Integer),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('DaysSinceRelease', Integer),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('FW1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FW2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FA_ID', Integer),
    Column('FA', Unicode(255)),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CreationDate', DateTime)
)


t_V_Qry_Released_MaxStation@60Days = Table(
    'V_Qry_Released_MaxStation@60Days', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('Date@XDays', DateTime),
    Column('MonitoringStatus@XDays', Unicode(1000)),
    Column('SurveyType@XDays', Unicode(1000)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('CurrentPTTModel', Unicode(150)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('Sex', Unicode(150)),
    Column('BreedingRing', Unicode(100)),
    Column('ReleaseRing', Unicode(100)),
    Column('ChipCode', Unicode(100)),
    Column('Mark1Color', Unicode(150)),
    Column('Mark1Position', Unicode(150)),
    Column('Mark1Code', Unicode(100)),
    Column('Mark2Color', Unicode(150)),
    Column('Mark2Position', Unicode(150)),
    Column('Mark2Code', Unicode(100)),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('RelMethod_ID', Integer),
    Column('RelMethod', Unicode(250)),
    Column('RelSta_ID', Integer),
    Column('RelStaName', Unicode(255)),
    Column('RelStaDate', DateTime),
    Column('RelRegion', Unicode(255)),
    Column('RelPlace', Unicode(50)),
    Column('StaType', String(11, 'French_CI_AS')),
    Column('Sta_ID', Integer),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('DaysSinceRelease', Integer),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('FW1', Integer),
    Column('FW2', Integer),
    Column('FA_ID', Integer),
    Column('FA', Unicode(255)),
    Column('Creator', Integer),
    Column('CreationDate', DateTime)
)


t_V_Qry_Released_MaxStation@90Days = Table(
    'V_Qry_Released_MaxStation@90Days', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('Date@XDays', DateTime),
    Column('MonitoringStatus@XDays', Unicode(1000)),
    Column('SurveyType@XDays', Unicode(1000)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('CurrentPTTModel', Unicode(150)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('Sex', Unicode(150)),
    Column('BreedingRing', Unicode(100)),
    Column('ReleaseRing', Unicode(100)),
    Column('ChipCode', Unicode(100)),
    Column('Mark1Color', Unicode(150)),
    Column('Mark1Position', Unicode(150)),
    Column('Mark1Code', Unicode(100)),
    Column('Mark2Color', Unicode(150)),
    Column('Mark2Position', Unicode(150)),
    Column('Mark2Code', Unicode(100)),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('RelMethod_ID', Integer),
    Column('RelMethod', Unicode(250)),
    Column('RelSta_ID', Integer),
    Column('RelStaName', Unicode(255)),
    Column('RelStaDate', DateTime),
    Column('RelRegion', Unicode(255)),
    Column('RelPlace', Unicode(50)),
    Column('StaType', String(11, 'French_CI_AS')),
    Column('Sta_ID', Integer),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('DaysSinceRelease', Integer),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('FW1', Integer),
    Column('FW2', Integer),
    Column('FA_ID', Integer),
    Column('FA', Unicode(255)),
    Column('Creator', Integer),
    Column('CreationDate', DateTime)
)


t_V_Qry_Released_MaxStation@XDays = Table(
    'V_Qry_Released_MaxStation@XDays', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('Date@XDays', DateTime),
    Column('MonitoringStatus@XDays', Unicode(1000)),
    Column('SurveyType@XDays', Unicode(1000)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('CurrentPTTModel', Unicode(150)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('Sex', Unicode(150)),
    Column('BreedingRing', Unicode(100)),
    Column('ReleaseRing', Unicode(100)),
    Column('ChipCode', Unicode(100)),
    Column('Mark1Color', Unicode(150)),
    Column('Mark1Position', Unicode(150)),
    Column('Mark1Code', Unicode(100)),
    Column('Mark2Color', Unicode(150)),
    Column('Mark2Position', Unicode(150)),
    Column('Mark2Code', Unicode(100)),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('RelMethod_ID', Integer),
    Column('RelMethod', Unicode(250)),
    Column('RelSta_ID', Integer),
    Column('RelStaName', Unicode(255)),
    Column('RelStaDate', DateTime),
    Column('RelRegion', Unicode(255)),
    Column('RelPlace', Unicode(50)),
    Column('StaType', String(11, 'French_CI_AS')),
    Column('Sta_ID', Integer),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('DaysSinceRelease', Integer),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('FW1', Integer),
    Column('FW2', Integer),
    Column('FA_ID', Integer),
    Column('FA', Unicode(255)),
    Column('Creator', Integer),
    Column('CreationDate', DateTime)
)


t_V_Qry_Released_Not_Houbara_FirstStation = Table(
    'V_Qry_Released_Not_Houbara_FirstStation', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('CurrentPTTModel', Unicode(150)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('Sex', Unicode(150)),
    Column('BreedingRing', Unicode(100)),
    Column('ReleaseRing', Unicode(100)),
    Column('ChipCode', Unicode(100)),
    Column('Mark1Color', Unicode(150)),
    Column('Mark1Position', Unicode(150)),
    Column('Mark1Code', Unicode(100)),
    Column('Mark2Color', Unicode(150)),
    Column('Mark2Position', Unicode(150)),
    Column('Mark2Code', Unicode(100)),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('WeightGrs', Float(53)),
    Column('Skull', Float(53)),
    Column('Tarso_Metatarsus', Float(53)),
    Column('RelMethod_ID', Integer),
    Column('RelMethod', Unicode(250)),
    Column('RelComments', Integer),
    Column('StaType', String(7, 'French_CI_AS'), nullable=False),
    Column('Sta_ID', Integer, nullable=False),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('DaysSinceRelease', Integer, nullable=False),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('FW1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FW2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FA_ID', Integer),
    Column('FA', Unicode(255)),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CreationDate', DateTime),
    Column('IndivComments', Unicode(255)),
    Column('BiometryComments', Unicode(150))
)


t_V_Qry_StationsForMap = Table(
    'V_Qry_StationsForMap', metadata,
    Column('TSta_PK_ID', Integer, nullable=False),
    Column('FieldWorker1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FieldWorker2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NbFieldWorker', Integer),
    Column('FieldActivity_Name', Unicode(255)),
    Column('Name', Unicode(255)),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('DATE', DateTime),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('ELE', Integer),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Creation_date', DateTime),
    Column('TSta_FK_TGeo_ID', Integer),
    Column('Site_name', Unicode(50)),
    Column('Site_idType', Integer),
    Column('Site_type', Unicode(200)),
    Column('FieldActivity_ID', Integer)
)


t_V_Qry_VGroups_AllTaxons_AllStations = Table(
    'V_Qry_VGroups_AllTaxons_AllStations', metadata,
    Column('TSta_PK_ID', Integer, nullable=False),
    Column('Name', Unicode(255)),
    Column('DATE', DateTime),
    Column('FieldWorker1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FieldWorker2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FieldActivity_Name', Unicode(255)),
    Column('NbFieldWorker', Integer),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('ELE', Integer),
    Column('Precision', Integer),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Site_name', Unicode(50)),
    Column('Site_type', Unicode(200)),
    Column('Name_Taxon', Unicode(250)),
    Column('LatinName', Unicode),
    Column('class', Unicode(255)),
    Column('Nb_Adult_Female', Integer),
    Column('Nb_Adult_Male', Integer),
    Column('Nb_Adult_Indeterminate', Integer),
    Column('Nb_Indeterminate', Integer),
    Column('Nb_Juvenile_Female', Integer),
    Column('Nb_Juvenile_Indeterminate', Integer),
    Column('Nb_Juvenile_Male', Integer),
    Column('Nb_NewBorn_Indeterminate', Integer),
    Column('Nb_Total', Integer),
    Column('Name_Behaviour', Unicode(250)),
    Column('Comments', Unicode(300)),
    Column('Identity_sure', BIT, nullable=False),
    Column('GroupPK', Integer, nullable=False)
)


t_V_Qry_VGroups_AllTaxons_EnjilDamStations = Table(
    'V_Qry_VGroups_AllTaxons_EnjilDamStations', metadata,
    Column('Monitored_station_name', Unicode(50)),
    Column('Station_Name', Unicode(255)),
    Column('DATE', DateTime),
    Column('English_name', Unicode(250)),
    Column('Latin_name', Unicode),
    Column('French_Name_Taxon', Unicode(255)),
    Column('Number_of_individuals', Integer),
    Column('TSta_PK_ID', Integer, nullable=False),
    Column('FieldWorker1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FieldWorker2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NbFieldWorker', Integer),
    Column('FieldActivity_Name', Unicode(255)),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('ELE', Integer),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Creation_date', DateTime),
    Column('TSta_FK_TGeo_ID', Integer),
    Column('Site_idType', Integer),
    Column('Site_type', Unicode(200)),
    Column('FieldActivity_ID', Integer)
)


t_V_Qry_VHF_FirstStation = Table(
    'V_Qry_VHF_FirstStation', metadata,
    Column('ind_id', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('CurrentVHFSN', Unicode(100)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('VHFSN@Station', Unicode(250)),
    Column('StaType', String(11, 'French_CI_AS')),
    Column('Sta_ID', Integer),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('DaysSinceFirstStation', Integer),
    Column('Region', Unicode(255))
)


t_V_Qry_VHF_LastStation = Table(
    'V_Qry_VHF_LastStation', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('CurrentVHFSN', Unicode(100)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('StaType', String(11, 'French_CI_AS')),
    Column('Sta_ID', Integer),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('DaysSinceFirstStation', Integer),
    Column('Region', Unicode(255))
)


t_V_Qry_VIndiv_MonitoredLostPostReleaseIndividuals_LastStations = Table(
    'V_Qry_VIndiv_MonitoredLostPostReleaseIndividuals_LastStations', metadata,
    Column('Name', Unicode(255)),
    Column('Site_name', Unicode(50)),
    Column('StaType', String(11, 'French_CI_AS')),
    Column('StaName', Unicode(255)),
    Column('label', Unicode(30)),
    Column('Fk_TInd_ID', Integer, nullable=False),
    Column('Frequency', Integer),
    Column('FreqOpti', Integer),
    Column('RelCaptTag', Unicode(100)),
    Column('species_id', Integer),
    Column('species', Unicode(150)),
    Column('id34@TCaracThes_Species_Precision', Unicode(150)),
    Column('BreedingRingCode', Unicode(100)),
    Column('SurveyType@Station', Unicode(1000)),
    Column('MonitoringStatus@Station', Unicode(1000)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('Origin', Unicode(150)),
    Column('Sex', Unicode(150)),
    Column('TSta_PK_ID', Integer, nullable=False),
    Column('FieldWorker1', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FieldWorker2', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NbFieldWorker', Integer),
    Column('FieldActivity_Name', Unicode(255)),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('DATE', DateTime),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('ELE', Integer),
    Column('Creator', String(201, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Creation_date', DateTime),
    Column('TSta_FK_TGeo_ID', Integer),
    Column('Site_Idtype', Integer),
    Column('Site_type', Unicode(200)),
    Column('FieldActivity_ID', Integer),
    Column('Name_signal_type', Unicode(250))
)


class VSearchIndiv(Base):
    __tablename__ = 'V_Search_Indiv'

    id = Column(Integer, primary_key=True)
    ptt = Column(Integer)
    releaseYear = Column(Integer)
    captureYear = Column(Integer)


t_V_qry_all_locations_all_indiv_semestrial = Table(
    'V_qry_all_locations_all_indiv_semestrial', metadata,
    Column('Ind_ID', Integer, nullable=False),
    Column('Origin', Unicode(150)),
    Column('Taxon', Unicode(150)),
    Column('CurrentIndividualStatus', Unicode(250)),
    Column('CurrentSurveyType', Unicode(150)),
    Column('CurrentMonitoringStatus', Unicode(150)),
    Column('CurrentPTT', Integer),
    Column('CurrentPTTModel', Unicode(150)),
    Column('PTT@Station', Unicode(250)),
    Column('PTTModel@Station', Unicode(1000)),
    Column('VHF@Station', Unicode(250)),
    Column('VHFModel@Station', Unicode(1000)),
    Column('CurrentVHF', Integer),
    Column('CurrentVHFModel', Unicode(150)),
    Column('MonitoringStatus@Station', Unicode(1000)),
    Column('SurveyType@Station', Unicode(1000)),
    Column('Sex', Unicode(150)),
    Column('ReleaseRing', Unicode(100)),
    Column('Ring', Unicode(100)),
    Column('ChipCode', Unicode(100)),
    Column('BirthDate', DateTime),
    Column('DeathDate', DateTime),
    Column('RelCaptSta_ID', Integer),
    Column('RelCaptStaType', String(7, 'French_CI_AS')),
    Column('RelCaptStaDate', DateTime),
    Column('RelCaptYear', Integer),
    Column('RelCaptRegion', Unicode(255)),
    Column('RelCaptPlace', Unicode(50)),
    Column('RelCaptLAT', Numeric(9, 5)),
    Column('RelCaptLON', Numeric(9, 5)),
    Column('StaType', String(11, 'French_CI_AS'), nullable=False),
    Column('Sta_ID', Integer, nullable=False),
    Column('StaName', Unicode(255)),
    Column('StaDate', DateTime),
    Column('Region', Unicode(255)),
    Column('Place', Unicode(50)),
    Column('LAT', Numeric(9, 5)),
    Column('LON', Numeric(9, 5)),
    Column('Precision', Integer),
    Column('FW1', Integer),
    Column('FW2', Integer),
    Column('FA_ID', Integer),
    Column('FA', Unicode(255))
)


t_geo_CNTRIES_and_RENECO_MGMTAreas = Table(
    'geo_CNTRIES_and_RENECO_MGMTAreas', metadata,
    Column('ID', Integer, nullable=False),
    Column('OBJECTID', BigInteger),
    Column('Place', Unicode(255)),
    Column('Country', Unicode(255)),
    Column('SHAPE_Leng', Float(24)),
    Column('SHAPE_Area', Float(24)),
    Column('geom', NullType),
    Column('valid_geom', NullType),
    Column('Reneco_Country', BIT, nullable=False)
)


t_geo_utm_grid_20x20_km = Table(
    'geo_utm_grid_20x20_km', metadata,
    Column('ogr_fid', Integer, nullable=False),
    Column('ogr_geometry', NullType, nullable=False),
    Column('code', String(6, 'French_CI_AS')),
    Column('utm_zone', Numeric(4, 0)),
    Column('xmin_wgs84', Numeric(19, 11)),
    Column('ymin_wgs84', Numeric(19, 11)),
    Column('xmax_wgs84', Numeric(19, 11)),
    Column('ymax_wgs84', Numeric(19, 11)),
    Column('intrv_area', String(50, 'French_CI_AS')),
    Column('x', Numeric(19, 11)),
    Column('y', Numeric(19, 11)),
    Column('x_ddm', String(50, 'French_CI_AS')),
    Column('y_ddm', String(50, 'French_CI_AS'))
)


t_geometry_columns = Table(
    'geometry_columns', metadata,
    Column('f_table_catalog', String(128, 'French_CI_AS'), nullable=False),
    Column('f_table_schema', String(128, 'French_CI_AS'), nullable=False),
    Column('f_table_name', String(256, 'French_CI_AS'), nullable=False),
    Column('f_geometry_column', String(256, 'French_CI_AS'), nullable=False),
    Column('coord_dimension', Integer, nullable=False),
    Column('srid', Integer, nullable=False),
    Column('geometry_type', String(30, 'French_CI_AS'), nullable=False)
)


t_spatial_ref_sys = Table(
    'spatial_ref_sys', metadata,
    Column('srid', Integer, nullable=False),
    Column('auth_name', String(256, 'French_CI_AS')),
    Column('auth_srid', Integer),
    Column('srtext', String(2048, 'French_CI_AS')),
    Column('proj4text', String(2048, 'French_CI_AS'))
)


class Sysdiagram(Base):
    __tablename__ = 'sysdiagrams'
    __table_args__ = (
        Index('UK_principal_name', 'principal_id', 'name', unique=True),
    )

    name = Column(Unicode(128), nullable=False)
    principal_id = Column(Integer, nullable=False)
    diagram_id = Column(Integer, primary_key=True)
    version = Column(Integer)
    definition = Column(VARBINARY(-1))
