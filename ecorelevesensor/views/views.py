from collections import OrderedDict
from pyramid.view import view_config

from sqlalchemy import (
		Float,
		between,
		func,
		cast,
		Date,
		select,
		join,
		and_,
		insert,
		bindparam
		)

import datetime, operator
import re, csv

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus.flowables import PageBreak
from reportlab.lib import colors
import numpy
from ..models import DBSession, Base
from ecorelevesensor.models.data import (
		Station,
		ViewRfid,
		ThemeEtude,
		MapSelectionManager,
		Protocole,
)
from ecorelevesensor.models import (
		MonitoredSite,
		User
)
from ecorelevesensor.models.sensor import Argos, Gps
from ecorelevesensor.utils.spreadsheettable import SpreadsheetTable

# Data imported from the CLS WS during the last week.
@view_config(route_name='weekData', renderer='json')
def weekData(request):
		"""Return an array of location number per day within the last seven days."""
		today = datetime.date.today()
		# Initialize Json object
		data = {
				'label':[str(today - datetime.timedelta(days = i)) for i in range(1,8)],
				'nbArgos': [0] * 7,
				'nbGPS': [0] * 7
		}

		# Argos data
		argos_query = select(
				[cast(Argos.date, Date).label('date'), func.count(Argos.id).label('nb')]
				).where(Argos.date >= today - datetime.timedelta(days = 7)
				).group_by(cast(Argos.date, Date)
		)
		for date, nb in DBSession.execute(argos_query).fetchall():
				try:
						i = data['label'].index(str(date))
						data['nbArgos'][i] = nb
				except: pass

		# GPS data
		gps_query = select(
				[cast(Gps.date, Date).label('date'), func.count(Gps.id).label('nb')]
				).where(Gps.date >= today - datetime.timedelta(days = 7)
				).group_by(cast(Gps.date, Date))
		for date, nb in DBSession.execute(gps_query).fetchall():
				try:
						i = data['label'].index(str(date))
						data['nbGPS'][i] = nb
				except: pass

		return data

@view_config(route_name = 'station_graph', renderer = 'json')
def station_graph(request):
		# Initialize Json object
		result = OrderedDict()

		# Calculate the bounds
		today = datetime.date.today()
		begin_date = datetime.date(day=1, month=today.month, year=today.year-1)
		end_date = datetime.date(day=1, month=today.month, year=today.year)

		# Query
		query = select([
				func.count(Station.id).label('nb'),
				func.year(Station.date).label('year'),
				func.month(Station.date).label('month')]
				).where(and_(Station.date >= begin_date, Station.date < end_date)
				).group_by(func.year(Station.date), func.month(Station.date)
		)

		"""
				Execute query and sort result by year, month
				(faster than an order_by clause in this case)
		"""
		data = DBSession.execute(query).fetchall()
		for nb, y, m in sorted(data, key=operator.itemgetter(1,2)):
				d = datetime.date(day=1, month=m, year=y).strftime('%b')
				result[' '.join([d, str(y)])] = nb

		return result

@view_config(route_name = 'theme/list', renderer = 'json')
def theme_list(request):
	 data = []
	 try:
			j = join(ThemeEtude, MapSelectionManager, ThemeEtude.id == MapSelectionManager.TSMan_FK_Theme)
			query = select([ThemeEtude.id, ThemeEtude.Caption]).where(ThemeEtude.Actif == 1).group_by(ThemeEtude.id, ThemeEtude.Caption).order_by(ThemeEtude.Caption)
			try:
				 if(request.GET['export'] is not None):
						query = query.select_from(j)
			except:
				 pass
			for id, caption in DBSession.execute(query).fetchall():
				 data.append({'id':id, 'caption': caption})
			try:
				 if(request.GET['export'] is not None):
						data.append({'id':'null', 'caption': 'Others'})
			except:
				 pass
	 except Exception as e:
			print(e)
	 return data

@view_config(route_name = 'core/protocoles/list', renderer = 'string')
def protocoles_list(request):
	xml = "<protocoles>"
	try:
		protocol=DBSession.execute(select([Protocole.id, Protocole.Relation, Protocole.Caption, Protocole.Description]).order_by(Protocole.Caption)).fetchall()
		for id, relation, caption, description in protocol:
			xml = xml + "<protocole id='"+str(id)+"'>"+caption+"</protocole>"
		xml = xml + "</protocoles>"
	except Exception as e:
		print ("________________ prtocole_list error :")
		print(e)
	request.response.content_type = "text/xml"
	print ("________________ prtocole_list")
	print (xml)
	return xml

@view_config(route_name = 'core/views/list', renderer = 'string')
def views_list(request):
	 xml = "<views>"
	 try:
			query = select([MapSelectionManager.id, MapSelectionManager.TSMan_sp_name, MapSelectionManager.TSMan_Layer_Name, MapSelectionManager.TSMan_Description, MapSelectionManager.TSMan_FK_Theme]).order_by(MapSelectionManager.TSMan_Layer_Name)
			try:
				 if request.GET['id_theme'] is not None:
						query = query.where(MapSelectionManager.TSMan_FK_Theme == request.GET['id_theme'])
			except Exception as e:
				 print(e)
			for id, sp_name, layer_name, description, fk_theme in DBSession.execute(query).fetchall():
				 xml = xml + "<view id='"+sp_name+"'>"+layer_name.replace("_", " ")+"</view>"
			xml = xml + "</views>"
	 except Exception as e:
			print(e)
	 request.response.content_type = "text/xml"
	 return xml

@view_config(route_name = 'core/views/export/details', renderer = 'json')
def views_details(request):
	 data = []
	 try:
			name_vue = request.matchdict['name']
			table = Base.metadata.tables[name_vue]
			print(table)
			for column in table.c:
				 name_c = str(column.name)
				 type_c = str(column.type)
				 if re.compile('VARCHAR').search(type_c):
						type_c = 'string'
				 data.append({'name':name_c, 'type':type_c})
			return data
	 except Exception as e:
	 	print(e)

@view_config(route_name = 'core/views/export/count', renderer = 'json')
def views_count(request):
	 try:
			name_vue = request.matchdict['name']
			table = Base.metadata.tables[name_vue]
			count = DBSession.execute(table.count()).scalar()
			return count
	 except Exception as e:
			print(e)

@view_config(route_name = 'core/views/export/filter/count', renderer = 'json')
def views_filter_count(request):
	 try:
			name_vue = request.matchdict['name']
			table = Base.metadata.tables[name_vue]
			criteria = request.params
			query = select([func.count(table.c.values()[0])])
			query = query_criteria(query, table, criteria)

			count = DBSession.execute(query).scalar()
			return count
	 except Exception as e:
			print(e)

@view_config(route_name = 'core/views/export/filter/geo', renderer = 'json')
def views_filter(request):
	 try:
			name_vue = request.matchdict['name']
			table = Base.metadata.tables[name_vue]
			criteria = request.params
			result = {'type':'FeatureCollection', 'features':[]}
			query = select([cast(table.c['LAT'].label('lat'), Float), cast(table.c['LON'].label('lon'), Float), func.count(table.c.values()[0])]).group_by(table.c['LAT'].label('lat'), table.c['LON'])
			query = query_criteria(query, table, criteria)
			for lat, lon, nb in  DBSession.execute(query).fetchall():
				 result['features'].append({'type':'Feature', 'properties':{'count': nb}, 'geometry':{'type':'Point', 'coordinates':[lon,lat]}})
			return result
	 except Exception as e:
			print(e)

@view_config(route_name = 'core/views/export/filter/result', renderer = 'json')
def views_filter_result(request):
	 try:
			name_vue = request.matchdict['name']
			table = Base.metadata.tables[name_vue]
			criteria = request.params
			skip = 0
			limit = 10
			try:
				 if criteria['skip']:
						skip = int(criteria['skip'])
			except:
				 pass
			try:
				 if criteria['limit']:
						limit = int(criteria['limit'])
			except:
				 pass
			columns = []
			cols = []
			if criteria['columns']:
				 columns.append(func.row_number().over(order_by=table.c.values()[0].asc()).label('Id'))
				 cols = criteria['columns'].split(',')
				 for col in cols:
						columns.append(table.c[col])

			#count
			query_count = select([func.count(table.c.values()[0])])
			query_count = query_criteria(query_count, table, criteria)
			count = DBSession.execute(query_count).scalar()
			# select data
			query = select(columns)
			query = query_criteria(query, table, criteria)
			query = query.order_by(table.c.values()[0].asc()).limit(limit).offset(skip)

			data = DBSession.execute(query).fetchall()
			result = {'count':str(count), 'values':[]}
			result['values'] = [dict(row) for row in data]
			for obj in result['values']:
				 for key, item in obj.items():
							 obj[key] = item
			return result
	 except Exception as e:
			print(e)


def query_criteria(query, table, criteria):
	 for column, value in criteria.items():
				 if column in table.c:
						if re.search(',',value):
							 sp = value.split(',')
							 if sp[0] == 'IN':
									if re.search('|',sp[1]):
										 data = sp[1].split('|')
									else:
										 data = sp[1]
									query = query.where(table.c[column].in_(data))
							 elif sp[0] == 'LIKE':
									query = query.where(table.c[column].like('%'+sp[1]+'%'))
							 elif sp[0] == '<':
									query = query.where(table.c[column] < sp[1])
							 elif sp[0] == '>':
									query = query.where(table.c[column] > sp[1])
							 elif sp[0] == '<>':
									query = query.where(table.c[column] != sp[1])
							 elif sp[0] == '=':
									query = query.where(table.c[column] == sp[1])
						else:
							 if value == 'IS NULL':
									query = query.where(table.c[column].is_(None))
							 elif value == 'IS NOT NULL':
									query = query.where(table.c[column].isnot(None))
				 else:
						if column == 'bbox':
							 sp = value.split(',')
							 query = query.where(and_(between(table.c['LAT'], float(sp[1]), float(sp[3])), between(table.c['LON'], float(sp[0]), float(sp[2]))))
	 return query
