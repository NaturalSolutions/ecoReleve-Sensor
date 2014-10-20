
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


from ..models import DBSession, Base
from pyramid.response import Response
from ecorelevesensor.models.sensor import Argos, Gps
from ecorelevesensor.utils.spreadsheettable import SpreadsheetTable
from ecorelevesensor.renderers.csvrenderer import CSVRenderer
from ecorelevesensor.renderers.pdfrenderer import PDFrenderer
from ecorelevesensor.renderers.gpxrenderer import GPXRenderer
from ecorelevesensor.views.views import query_criteria


@view_config(route_name = 'core/views/export/filter/export', request_method='POST')
def views_filter_export(request):

	type_export = request.json_body.get('type_export', {})
	function_export= { 'csv': export_csv,
	'pdf': export_pdf,
	'gpx': export_gpx}

	try:

		print ('in export with value : '+type_export)
		name_vue = request.matchdict['name']
		table = Base.metadata.tables[name_vue]
		criteria = request.params
		today = datetime.datetime.today().strftime('%d_%m_%Y %H_%M_%S')
		name_file = name_vue+"_"+today
		columns = []
		cols = []
		if criteria['columns']:
			cols = criteria['columns'].split(',')
			for col in cols:
				columns.append(table.c[col])
		query = select(columns)
		query = query_criteria(query, table, criteria)
		rows = DBSession.execute(query).fetchall()
		filename = name_vue+'.'+type_export
		request.response.content_disposition = 'attachment;filename=' + filename
		value={'header': cols,
		'rows': rows}

		io_export=function_export[type_export](value,request,name_vue)
		return Response(io_export)
	except: raise

def export_csv (value,request,name_vue) :
	csvRender=CSVRenderer()
	csv=csvRender(value,{'request':request})
	return csv

def export_pdf (value,request,name_vue):
	pdfRender=PDFrenderer()
	pdf=pdfRender(value,name_vue,request)
	return pdf

def export_gpx (value,request,name_vue):
	gpxRender=GPXRenderer()
	gpx=gpxRender(value,request)
	return gpx


  

	  

  