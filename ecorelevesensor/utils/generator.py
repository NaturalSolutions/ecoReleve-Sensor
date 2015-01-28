import operator, transaction
from sqlalchemy import *
import json,transaction
from ecorelevesensor.models import Base, DBSession
from collections import OrderedDict


class Generator :
    def __init__(self,table):
        print('-------------------columnGENERATOR-------------------')

        self.dictCell={
            'VARCHAR':'string',
            'NVARCHAR':'string',
            'INTEGER':'integer',
            'DECIMAL':'number',
            'DATETIME':'date',
            'BIT':'boolean'
            }
        self.table=Base.metadata.tables[table]
        self.cols=[]

    def get_operator_fn(self,op):
        return {
            '<' : operator.lt,
            '>' : operator.gt,
            '=' : operator.eq,
            '<>': operator.ne,
            '<=': operator.le,
            '>=': operator.ge,
            'Like': operator.eq,
            'Not Like': operator.ne,
            }[op]

    def eval_binary_expr(self,op1, operator, op2):
        op1,op2 = op1, op2
        if 'date' in str(op1.type).lower() :
            op1=cast(op1,Date)
        return self.get_operator_fn(operator)(op1, op2)
    
    def get_col(self,columnsList=False, checked=False):
        
        ###### model of columnsList #####


        final=[]

        for obj in columnsList :

            field_name=obj['name']
            field_label=obj['label']
            display=obj['display']
            edit=obj['edit']

            field_type=str(self.table.c[field_name].type).split('(')[0]

            if field_type in self.dictCell:        
                cell_type=self.dictCell[field_type]  
            else:
                cell_type='string'

            final.append({'name':field_name,
                'label':field_label,
                'cell':cell_type,
                'renderable':display,
                'editable':edit})

            self.cols.append({'name':field_name,'type_grid':cell_type})

        if(checked):
            final.append({'name': 'import','label': 'Import', 'cell': 'select-row', 'headerCell' : 'select-all'})

        return final

    def where (self,query,col,operator,value):

        return query.where(self.eval_binary_expr(self.table.c[col], operator, value))


    def get_search(self,criteria={},offset=None,per_page=None, order_by=None) :

        query = select(self.table.c)
        result=[]
        total=None

        for obj in criteria:

            print('__________________')
            print(obj['Value'])
            if obj['Value'] != None and obj['Value']!='':

                try:
                    Col=dictio[key]
                except: 
                    Col=obj['Column']
                
                query=self.where(query,Col, obj['Operator'], obj['Value'])

        if offset!=None:
            query, total=self.get_page(query,offset,per_page, order_by)

        data = DBSession.execute(query).fetchall()
        
        if(total or total == 0):
            result = [{'total_entries':total}]
            result.append([OrderedDict(row) for row in data])
        else :
            result = [OrderedDict(row) for row in data]
        transaction.commit()
        return result


    def get_page(self,query,offset,limit,order_by):

        total = DBSession.execute(select([func.count()]).select_from(query.alias())).scalar()
        order_by_clause = []



        for obj in order_by:
            column, order = obj.split(':')
            #if column in dictio :
            #    column=dictio[column]
            if column in self.table.c:
                if order == 'asc':
                    order_by_clause.append(self.table.c[column].asc())
                elif order == 'desc':
                    order_by_clause.append(self.table.c[column].desc())
        if len(order_by_clause) > 0:
            query = query.order_by(*order_by_clause)
        else :
            col= self.table.c[self.table.c.__dict__['_all_columns'][0].name].asc()
            query = query.order_by(col)

        # Define the limit and offset if exist
        if limit > 0:
            query = query.limit(limit)
        if offset > 0:
            query = query.offset(offset)

        return query, total

    def update_data(self,model,id_name) : 
        print('______UPDATE ! ___________')

        id_=model[id_name]
        print(model['patch'])
        if model['patch']!={} :   
            r=update(self.table).where(self.table.c[id_name]==id_).values(model['patch'])
            DBSession.execute(r)
    
    def get_geoJSON(self,criteria={},offset=None,per_page=None, order_by=None) :

        query = select(self.table.c)
        result=[]
        total=None

        print(criteria)
        '''
        for obj in criteria:

            query=query.where(eval_binary_expr(table.c[obj['Column']], obj['Operator'], obj['Value']))

        '''
        for obj in criteria:
            print('__________________')
            print(obj['Value'])
            if obj['Value'] != None and obj['Value']!='':
                
                
                try:
                    Col=dictio[key]
                except: 
                    Col=obj['Column']
                
                query=query.where(self.eval_binary_expr(self.table.c[Col], obj['Operator'], obj['Value']))

        '''
        if offset!=None:
            query, total=self.get_page(query,offset,per_page, order_by)
        '''

        data=DBSession.execute(query).fetchall()    

        geoJson=[]
        for row in data:
            geoJson.append({'type':'Feature', 'properties':{'name':row['Name']}, 'geometry':{'type':'Point', 'coordinates':[row['LON'],row['LAT']]}})


        transaction.commit()
        return {'type':'FeatureCollection', 'features': geoJson}
