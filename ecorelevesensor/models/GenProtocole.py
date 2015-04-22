from ..models import Base, DBSession, User
from sqlalchemy import select

class GenProtocole ():

	def InitFromFields (self,GivenFields):

		# dictionnary to retrieve ID from Thesaurus
		sex_value={'sex>male':18873,
				'sex>female': 18874,
				'sex>(indeterminate)':18875,
				'':None,
				'male':18873,
				'female': 18874,
				'(indeterminate)':18875}

		age_value={'age>newborn':18877,
				'age>juvenile': 18878,
				'age>adult':18879,
				'age>(indeterminate)':18880,
				'age>embryo (egg)':18993,
				'':None,
				'newborn':18877,
				'juvenile': 18878,
				'adult':18879,
				'(indeterminate)':18880,
				'embryo (egg)':18993}

		for Key,Value in  GivenFields.items():
			if Key not in ['PK','name','Id_Sex','id_sex','Id_Age','id_age','Id_Taxon','id_taxon'] :
				setattr(self,self.GetAttributeNameFromColumn(Key),Value)

			if (Key =='Name_Sex' or Key=='name_sex' and Val!=None) :
				
				try :
					setattr(self,self.GetAttributeNameFromColumn('Id_Sex'),sex_value[Value])
				except :
					setattr(self,self.GetAttributeNameFromColumn('id_sex'),sex_value[Value])
					continue

			if (Key =='Name_Age' or Key=='name_age' and Val!=None) :
				
				try :
					setattr(self,self.GetAttributeNameFromColumn('Id_Age'),age_value[Value])
				except :
					setattr(self,self.GetAttributeNameFromColumn('id_age'),age_value[Value])
					continue

			if (Key=='Name_Taxon' or Key=='name_taxon') :
				taxName=Value.split('>')[-1]
				Tthesaurus=Base.metadata.tables['Tthesaurus']
				query=select([Tthesaurus.c.ID]).where(Tthesaurus.c.topic_en==taxName)
				id_taxon=DBSession.execute(query).scalar()

				try :
					setattr(self,self.GetAttributeNameFromColumn('Id_Taxon'),id_taxon)
				except :
					setattr(self,self.GetAttributeNameFromColumn('id_taxon'),id_taxon)
					continue
				
	def GetAttributeNameFromColumn(self,ColumnName):
		return ColumnName

	

