"""Projects URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#from django.conf.urls import re_path
from django.urls import re_path as url
from CMS.views import *
from CMS.CMS_Scripts import subnet,dnsclient,connectssh
from Projects import settings
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.site.site_header = "Networking Dashboard"
admin.site.index_title = 'Networking Dashboard'
admin.site.site_title = "Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('projectlist/accounts/logout', include('django.contrib.auth.urls')),
    path('', index, name='index'),
    path('logmein/', logmein, name='logmein'),
    url(r'projects/(?P<slug>.+)/',projectsview, name='projects'),
    path('projectlist/', projectsview, name='projectlist'),
    url(r'sites/(?P<slug>.+)/',sitesview, name='sites'),
    url(r'sites/(?P<pk>\d+)$',sitesview, name='sites'),
    path('sitelist/',sitesview, name='sitelist'),
    path('siteupload/',siteupload, name='siteupload'),
    url(r'devices/(?P<pk>\d+)/(?P<site>.+)/(?P<project>.+)/', devicesview, name='devices'),
    url(r'devices/(?P<slug>.+)/',devicesview, name='devices'),
    url(r'devices/(?P<pk>\d+)$',devicesview, name='devices'),
    url(r'circuits/(?P<pk>\d+)/(?P<site>.+)/(?P<project>.+)/', circuitsview, name='circuits'),
    url(r'circuits/(?P<slug>.+)/',circuitsview, name='circuits'),
    url(r'circuits/(?P<pk>\d+)$',circuitsview, name='circuits'),
    path('devicelist/',devicesview, name='devicelist'),
    path('circuitlist/',circuitsview, name='circuitlist'),
    path('exportsites/',sitedownload, name='sitedownload'),
    path('exportdevices/',devicedownload, name='devicedownload'),
    path('exportcircuits/',circuitdownload, name='circuitdownload'),
    path('deviceupload/',deviceupload, name='deviceupload'),
    path('circuitupload/',circuitupload, name='circuitupload'),
    url(r'^delete/device/(?P<pk>\d+)$',delete_device, name='delete_device'),
    path('add_project/',add_project, name ='add_project'),
    path('add_site/',add_site, name ='add_site'),
    #path('add_device/',add_device, name ='add_device'),
    path('add_device/',add_device.as_view(), name ='add_device'),
    path('add_circuit/',add_circuit.as_view(), name ='add_circuit'),
    url(r'edit_site/(?P<datatype>.+)/(?P<pk>\d+)/',edit, name ='edit_site'),
    url(r'edit_device/(?P<datatype>.+)/(?P<pk>\d+)/',edit, name ='edit_device'),
    url(r'edit_circuit/(?P<datatype>.+)/(?P<pk>\d+)/',edit, name ='edit_circuit'),
    url(r'^delete/site/(?P<pk>\d+)$',delete_site, name='delete_site'),
    url(r'^delete/project/(?P<pk>\d+)$',delete_project, name='delete_project'),
    url(r'^sitecheck/(?P<site>.+)/(?P<project>.+)/(?P<checktype>.+)',checking, name='sitecheck'),
    url(r'^devicecheck/(?P<pk>\d+)/(?P<checktype>.+)',checking, name='devicecheck'),
    # url(r'^connect/(?P<pk>\d+)/(?P<project>.+)', connectssh.connectssh, name='ssh_connect'),
    url(r'^connect/(?P<pk>\d+)', ssh_connect, name='ssh_connect'),
    url(r'^devicebackup/(?P<pk>\d+)$',backup, name='devicebackup'),
    url(r'^sitebackup/(?P<site>.+)/(?P<project>.+)',backup, name='sitebackup'),
    path('ajax/load-sites/', load_sites, name='ajax_load_sites'),
    url(r'^tools/$',tool,name='tool'),
    url(r'^subnet/$',subnet.subnet,name='subnet'),
    url(r'^dnsreq/$',dnsclient.dnsreq,name='dnsreq'),

    

 ]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.FILE_URL, document_root=settings.FILE_ROOT)

