from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import *

class DeviceRecources(resources.ModelResource):
	Name = fields.Field(
		column_name='Name',
		attribute='Name')
	IP = fields.Field(
		column_name='IP',
		attribute='IP')
	Category = fields.Field(
		column_name='Category',
		attribute='Category')
	Project = fields.Field(
		column_name='Project',
		attribute='Project',
		widget=ForeignKeyWidget(Projects, field='Name'))
	Site = fields.Field(
		column_name='Site',
		attribute='Site',
		widget=ForeignKeyWidget(Sites, field='Name'))

	class Meta:
		model = Devices
		fields = ('Name','IP','Category','Project', 'Site', 'id')

class SiteRecources(resources.ModelResource):
	Name = fields.Field(
		column_name='Name',
		attribute='Name')
	Project = fields.Field(
		column_name='Project',
		attribute='Project',
		widget=ForeignKeyWidget(Projects, field='Name'))

	Country = fields.Field(
		column_name='Country',
		attribute='Country')

	class Meta:
		model = Sites
		fields = ('Name','Project','Country', 'id')

class CircuitRecources(resources.ModelResource):
	CircuitID = fields.Field(
		column_name='CircuitID',
		attribute='CircuitID')

	Bandwidth = fields.Field(
		column_name='Bandwidth',
		attribute='Bandwidth')

	WANIP = fields.Field(
		column_name='WANIP',
		attribute='WANIP')

	CircuitType = fields.Field(
		column_name='CircuitType',
		attribute='CircuitType')

	Project = fields.Field(
		column_name='Project',
		attribute='Project',
		widget=ForeignKeyWidget(Projects, field='Name'))
	
	Site = fields.Field(
		column_name='Site',
		attribute='Site',
		widget=ForeignKeyWidget(Sites, field='Name'))

	class Meta:
		model = Circuit
		fields = ('CircuitID','Bandwidth', 'WANIP','CircuitType','Project', 'Site', 'id')
