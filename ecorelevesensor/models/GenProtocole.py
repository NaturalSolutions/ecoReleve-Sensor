from ..models import Base, DBSession, User
from sqlalchemy import select

class GenProtocole ():
	def __init__(self):
		print('-------------------OK GenProtocole-------------------')
	def InitFromFields (self,GivenFields):
		for Key,Value in  GivenFields.items():
			if (Key != 'name'):
				setattr(self,self.GetAttributeNameFromColumn(Key),Value)
				print(' Set Attribute ' + Key + ':' + str(Value) )
			if (Key =='Name_Sex' or Key=='name_sex') :
				sex_value={'sex>male':18873,
				'sex>female': 18874,
				'sex>(indeterminate)':18875}
				try :
					setattr(self,self.GetAttributeNameFromColumn('Id_Sex'),sex_value[Value])
				except :
					setattr(self,self.GetAttributeNameFromColumn('id_sex'),sex_value[Value])
			if (Key =='Name_Age' or Key=='name_age') :
				sex_value={'age>newborn':18877,
				'age>juvenile': 18878,
				'age>adult':18879,
				'age>(indeterminate)':18880,
				'age>embryo (egg)':18993}
				try :
					setattr(self,self.GetAttributeNameFromColumn('Id_Age'),sex_value[Value])
				except :
					setattr(self,self.GetAttributeNameFromColumn('id_age'),sex_value[Value])
			if (Key=='Id_Observer' or Key=='Id_Assistant') :
				users_ID_query = select([User.id], User.fullname.in_((Value)))
				users_ID = DBSession.execute(users_ID_query).fetchone()
				setattr(self,self.GetAttributeNameFromColumn(Key),users_ID)

			if (Key=='Name_Taxon' or Key=='name_taxon') :
				taxName=Value.split('>')[-1]
				print (taxName)
				Tthesaurus=Base.metadata.tables['Tthesaurus']
				print (Tthesaurus.c["ID"])
				query=select([Tthesaurus.c.ID]).where(Tthesaurus.c.topic_en==taxName)
				print(query)
				id_taxon=DBSession.execute(query).fetchone()
				print (id_taxon)
				try :
					setattr(self,self.GetAttributeNameFromColumn('Id_Taxon'),id_taxon[0])
				except :
					setattr(self,self.GetAttributeNameFromColumn('id_taxon'),id_taxon[0])




				
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

