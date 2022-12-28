from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from CMS.models import Projects, Sites
from .resources import *
#from .cmdrunner import Connect
from CMS.CMS_Scripts.cmdrunner import Connect
from CMS.form import *
from django.http import HttpResponse
import csv
from tablib import Dataset
import time
from datetime import date
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from os import system
import os
import environ

env = environ.Env()
environ.Env.read_env()

# Create your views here.

def index(request):
	#photo = models.ImageField(upload_to="gallery")
	return	render(request,'index.html',{})

def tool(request):
	#photo = models.ImageField(upload_to="gallery")
	return	render(request,'tools.html',{})

@login_required	()
def logmein(request):
	return redirect	('projectlist')

############## View models #################
def projectsview(request):
	context = {

		'form':Projects.objects.all()
	}
	return render(request,'projects.html',context)

def devicesview(request, pk='0', site='0', project='0',):
	#access from device page filter by Project
	if pk != '0' and site =='0' and project !='0':
		form = Devices.objects.filter(Project__Name__exact=project)
		#sitename = Devices.objects.get(pk=pk).Site
		total = len(form)
		#sitename = Devices.objects.get(pk=pk).Site
		context = {
			'form':form,
			'projectname':project,
			'sitename':'All',
			'total':total,
			'checkall':'yes'
		}
	#access from device page filter by Site
	elif pk != '0' and site !='0' and project =='0':
		form = Devices.objects.filter(Site__Name__exact=site)
		projectname = Devices.objects.get(pk=pk).Project
		total=len(form)
		context = {
			'form':form,
			'projectname':projectname,
			'sitename':site,
			'total':total,
			'checkall':'yes'
		}
	##access from site page
	elif pk=='0' and site != '0' and project != '0':
		form = Devices.objects.filter(Site__Name__exact=site)
		s = Sites.objects.get(Name=site)
		total = len(form)
		context = {
			'form':form,
			'projectname':project,
			'sitename':site,
			'total':total,
			'checkall':'yes'
		}

	else:
		form = Devices.objects.all().order_by('Site')
		header = 'Device Summary'
		total=len(form)
		context = {
			'header':header,
			'form':form,
			'export':'Yes',
			'total':total
		}
	return render(request,'devices.html',context)

############### For Circuit #######################

def circuitsview(request, pk='0', site='0', project='0',):
	#access from device page filter by Project
	if pk != '0' and site =='0' and project !='0':
		form = Circuit.objects.filter(Project__Name__exact=project)
		#sitename = Devices.objects.get(pk=pk).Site
		total = len(form)
		#sitename = Devices.objects.get(pk=pk).Site
		context = {
			'form':form,
			'projectname':project,
			'sitename':'All',
			'total':total,
			'checkall':'yes'
		}
	#access from device page filter by Site
	elif pk != '0' and site !='0' and project =='0':
		form = Circuit.objects.filter(Site__Name__exact=site)
		projectname = Circuit.objects.get(pk=pk).Project
		total=len(form)
		context = {
			'form':form,
			'projectname':projectname,
			'sitename':site,
			'total':total,
			'checkall':'yes'
		}
	##access from site page
	elif pk=='0' and site != '0' and project != '0':
		form = Circuit.objects.filter(Site__Name__exact=site)
		s = Sites.objects.get(Name=site)
		total = len(form)
		context = {
			'form':form,
			'projectname':project,
			'sitename':site,
			'total':total,
			'checkall':'yes'
		}

	else:
		form = Circuit.objects.all().order_by('Site')
		header = 'Circuit Summary'
		total=len(form)
		context = {
			'header':header,
			'form':form,
			'export':'Yes',
			'total':total
		}
	return render(request,'circuits.html',context)


##################################

def sitesview(request, pk='0', slug='0'):

	form= Sites.objects.all()
	if pk=='0' and slug =='0':
		form = Sites.objects.all()
		header = 'Sites Summary'

	else:
		###view from project page
		if slug != '0':
			###view from site page per country
			form = Sites.objects.filter(Country=slug)
			header = 'Country: '+slug
		###view from project page
		if pk !='0':
			pkey=Projects.objects.get(pk=pk).Name
			form = Sites.objects.filter(Project__Name__contains=pkey)
			header = 'Project: '+str(pkey)
	total = len(form)
	context = {
		'form':form,
		'header':header,
		'total':total

	}

	return render(request,'sites.html',context)

################ Delete item ##############

@login_required(login_url='/accounts/login/')
def delete(request, pk, mtype, path):
	mtype.objects.filter(id=pk).delete()
	return redirect(path)

def delete_site(request,pk):
	path = '/sites/'+Sites.objects.get(pk=pk).Project.Name
	return delete(request,pk,Sites,path)


def delete_project(request,pk):
	return delete (request,pk,Projects,'/projectlist')

def delete_device(request,pk):
	return delete (request,pk,Devices,'/devicelist')

def delete_circuit(request,pk):
	return delete (request,pk,Circuit,'/circuitlist')

################ Add item ##############
@login_required	()
def add(request, data, mtype, path = '0'):
	if request.method == 'POST':
		form=data(request.POST)
		if mtype=='site':
			path = '/sitelist'
		if mtype=='project':
			path = '/projectlist/'
		if mtype=='device':
			path = '/devicelist/'
		if mtype=='circuit':
			path = '/circuitlist/'
		if form.is_valid():
			form.save()
			context = {
			'form': form
			}
			return redirect (path)
	else:
		context = {

		'form': data
		}
		return render(request,'add.html',context)


def add_site(request):
	form = site_form
	mtype = 'site'
	return add(request,form,mtype)


class add_circuit(CreateView):
	model= Circuit
	form_class = circuit_form
	success_url = reverse_lazy('circuitlist')

def add_project(request):
	form = project_form
	mtype = 'project'
	return add(request,form,mtype)

class add_device(CreateView):
	model= Devices
	form_class = device_form
	success_url = reverse_lazy('devicelist')

def load_sites(request):
	project_id = request.GET.get('Project')
	project_name = Projects.objects.get(pk=project_id)
	sites = Sites.objects.filter(Project_id =project_id).order_by('Name')
	return render(request, 'CMS/site_dropdown_list_options.html', {'sites': sites})

@login_required()
def edit(request,datatype,pk):
	if datatype == 'device':
		item = get_object_or_404(Devices,pk=pk)
	if datatype == 'circuit':
		item = get_object_or_404(Circuit,pk=pk)
	if datatype == 'site':
		item = get_object_or_404(Sites,pk=pk)

	if request.method == 'POST':
		if datatype == 'device':
			form = edit_device_form(request.POST, instance=item)
			path = 'devicelist'
		if datatype == 'circuit':
			form = edit_circuit_form(request.POST, instance=item)
			path = 'circuitlist'
		if datatype == 'site':
			form = site_form(request.POST, instance=item)
			path = 'sitelist'

		if form.is_valid():
			form.save()
			return redirect (path)
	else:
		if datatype == 'device':
			form = edit_device_form(instance=item)
		if datatype == 'circuit':
			form = edit_circuit_form(instance=item)
		if datatype == 'site':
			form = site_form(instance=item)

		return render(request, 'edit.html', {'form':form})


############### Import items #################
@login_required	()
def upload(request,mtype):
	if request.method == 'POST':
		if mtype == 'device':
			devices = DeviceRecources()
			path = 'devicelist'
			dataset = Dataset()
		if mtype == 'site':
			devices = SiteRecources()
			path = 'sitelist'
			dataset = Dataset()
		if mtype == 'circuit':
			devices = CircuitRecources()
			path = 'circuitlist'
			dataset = Dataset()
		new_items = request.FILES['myfile']
		imported_data = dataset.load(new_items.read().decode('utf-8'),format='csv')
		result = devices.import_data(dataset, dry_run=True)  # Test the data import
		if not result.has_errors():
			print('No errorrrrr')
		devices.import_data(dataset, dry_run=False)  # Actually import now
		return redirect(path)
	else:
		return render(request,'import.html')

def deviceupload(request):
	mtype = 'device'
	return(upload(request,mtype))

def siteupload(request):
	mtype = 'site'
	return(upload(request,mtype))

def circuitupload(request):
	mtype = 'circuit'
	return(upload(request,mtype))
############### Download Device list ##########
@login_required()
def download(request, mtype):
	if mtype == 'device':
		devices = DeviceRecources()
	if mtype =='site':
		devices = SiteRecources()
	if mtype =='circuit':
		devices = CircuitRecources()
	dataset = devices.export()
	response = HttpResponse(dataset.csv, content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="devices.csv"'
	return response
def devicedownload(request):
	mtype = 'device'
	return(download(request,mtype))
def sitedownload(request):
	mtype = 'site'
	return(download(request,mtype))

def circuitdownload(request):
	mtype = 'circuit'
	return(download(request,mtype))

############### Checking devices #############
def usernamepassword (project):
	name = str(project)
	username='%s_user'%name.lower()
	password=env('%s_pass'%name.lower())
	return (username, password)

#@login_required()
def checking(request, pk='0', site='0', project='0', job='0', checktype='0'):
	status=[]
	devicelist=[]
	d = date.today()
	day = d.strftime("%B %d, %Y")
	t = time.localtime()
	start_time = time.strftime("%H:%M:%S", t)
	if pk != '0': ##Check for the individual device
		device = Devices.objects.get(pk=pk)
		projectname = device.Project
		sitename = device.Site
		devicelist.append(device)
		username, password = usernamepassword(device.Project)
		if job =='backup':
			status=(Connect(devicelist,username,password,job, projectname, sitename))

		else:
			status=(Connect(devicelist,username,password,job, projectname, sitename,checktype))

	if site != '0' and site!="All": ##Check all devices in individual site
		devices = Devices.objects.filter(Site__Name__exact=site)
		username, password = usernamepassword(project)
		projectname = project
		sitename = site
		for device in devices:
			if job =='backup':
				if device.Category != 'WAN Optimizer':
					devicelist.append(device)
			else:
				devicelist.append(device)
		if job =='backup':
			status=(Connect(devicelist,username,password,job, projectname, sitename))
		else:
			status=(Connect(devicelist,username,password,job, projectname, sitename,checktype))
	if site == 'All' and project != '0': ###Check all devices in individual Project
		devices = Devices.objects.filter(Project__Name__exact=project)
		username, password = usernamepassword(project)
		projectname = project
		sitename = 'All'
		for device in devices:
			devicelist.append(device)
		if job =='backup':
			status=(Connect(devicelist,username,password,job, projectname, sitename))

		else:
			status=(Connect(devicelist,username,password,job, projectname, sitename,checktype))
	
	t = time.localtime()
	finish_time = time.strftime("%H:%M:%S", t)
	context = {
		'form':status,
		'date':day,
		'start_time':start_time,
		'finish_time':finish_time,
		'projectname':projectname,
		'sitename': sitename
	}
	print('############################################')
	print (status)
	return render(request,'status.html',context)

############### Backup device config ##################
@login_required()
def backup (request, pk='0', site='0', project='0'):
	return(checking(request, pk, site, project, job='backup'))

############### SSH Connect ############################
#@login_required()
def ssh_connect(request,pk='0'):
	device = Devices.objects.get(pk=pk)
	path = ".\\CMS\\CMS_resources\\files\\putty.exe"
	system('%s -ssh -2 %s'%(path,device.IP))
	return HttpResponse('', request)