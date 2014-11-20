from ..models import Base, DBSession, User
from sqlalchemy import select

class GenProtocole ():
	def __init__(self):
		print('-------------------OK GenProtocole-------------------')
	def InitFromFields (self,GivenFields):

		sex_value={'sex>male':18873,
				'sex>female': 18874,
				'sex>(indeterminate)':18875,
				'':None}

		age_value={'age>newborn':18877,
				'age>juvenile': 18878,
				'age>adult':18879,
				'age>(indeterminate)':18880,
				'age>embryo (egg)':18993,
				'':None}

		for Key,Value in  GivenFields.items():
			if (Key != 'name' or Key != 'PK'):
				setattr(self,self.GetAttributeNameFromColumn(Key),Value)
				print(' Set Attribute ' + Key + ':' + str(Value) )

			if (Key =='Name_Sex' or Key=='name_sex') :
				
				print(' Set Attribute Id_Sex:' + str(sex_value[Value]) )
				try :
					setattr(self,self.GetAttributeNameFromColumn('Id_Sex'),sex_value[Value])
				except :
					setattr(self,self.GetAttributeNameFromColumn('id_sex'),sex_value[Value])
					continue

			if (Key =='Name_Age' or Key=='name_age') :
				
				print(' Set Attribute Id_Age:' + str(age_value[Value]) )

				try :
					setattr(self,self.GetAttributeNameFromColumn('Id_Age'),age_value[Value])
				except :
					setattr(self,self.GetAttributeNameFromColumn('id_age'),age_value[Value])
					continue

			if (Key=='Id_Observer' or Key=='Id_Assistant') :
				users_ID_query = select([User.id], User.fullname.in_(([Value])))
				users_ID = DBSession.execute(users_ID_query).fetchone()
				try:
					setattr(self,self.GetAttributeNameFromColumn(Key),users_ID[0])
				except :
					setattr(self,self.GetAttributeNameFromColumn(Key),None)
					continue

			if (Key=='Name_Taxon' or Key=='name_taxon') :
				taxName=Value.split('>')[-1]
				print (taxName)
				Tthesaurus=Base.metadata.tables['Tthesaurus']
				print (Tthesaurus.c["ID"])
				query=select([Tthesaurus.c.ID]).where(Tthesaurus.c.topic_en==taxName)
				print(query)
				id_taxon=DBSession.execute(query).fetchone()
				print(' Set Attribute Id_Taxon:' + str(id_taxon) )

				try :
					setattr(self,self.GetAttributeNameFromColumn('Id_Taxon'),id_taxon[0])
				except :
					setattr(self,self.GetAttributeNameFromColumn('id_taxon'),id_taxon[0])
					continue




				
	def GetAttributeNameFromColumn(self,ColumnName):
		return ColumnName






# class SpecificProtocole(GenProtocole):
# 	def __init__(self):
# 		print('--------------------OK Specific-------------------')
# 	def GetAttributeNameFromColumn (self,ColumnName):
# 		print('Specific')
# 		if ColumnName=='Id_Sex':
# 			return 'Id_SexBezin'
# 		else:
# 			return super(SpecificProtocole, self).GetAttributeNameFromColumn(self,ColumnName)

