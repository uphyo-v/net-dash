from django.contrib import admin
from import_export.admin import ImportExportModelAdmin,ImportExportActionModelAdmin
from .models import *
from .resources import *
# Register your models here.
#admin.site.register(Projects)
#admin.site.register(Sites)
#admin.site.register(Devices)
@admin.register(Projects)
class DeviceAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
	resource_class = DeviceRecources
admin.site.register(Devices, DeviceAdmin)

class SiteAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
	resource_class = SiteRecources
admin.site.register(Sites, SiteAdmin)

class CircuitAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
	resource_class = CircuitRecources
admin.site.register(Circuit, SiteAdmin)

#@admin.register(Devices)
#class Devicesadmin(ImportExportModelAdmin):
#    pass