from ..models import Base

class GenProtocole ():
	def __init__(self):
		print('-------------------OK GenProtocole-------------------')
	def InitFromFields (self,GivenFields):
		for Key,Value in  GivenFields.items():
			if (Key != 'name'):
				setattr(self,self.GetAttributeNameFromColumn(Key),Value)
				print(' Set Attribute ' + Key + ':' + str(Value) )
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

