from django import forms
from .models import *

class site_form(forms.ModelForm):
	class Meta:
		model = Sites
		fields = ('Name','Country','Project', 'Contact')
		widgets = {
		'Name': forms.Textarea(attrs={'rows':1}),
		'Contact': forms.Textarea(attrs={'rows':2})
		}


class device_form(forms.ModelForm):
	class Meta:
		model = Devices
		fields = ('Name','IP','Category','Project','Site')
		widgets = {
		'Name': forms.Textarea(attrs={'rows':1}),
		'IP': forms.Textarea(attrs={'rows':1})
		}
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['Site'].queryset = Sites.objects.none()
		print(self.data)
		if 'Project' in self.data:
			try:
				Project_id = int(self.data.get('Project'))
				self.fields['Site'].queryset = Sites.objects.filter(Project_id=Project_id).order_by('Name')
			except (ValueError, TypeError):
				pass  # invalid input from the client; ignore and fallback to empty City queryset
		elif self.instance.pk:
			self.fields['Site'].queryset = self.instance.Project.Site_set.order_by('Name')

class edit_device_form(forms.ModelForm):
	class Meta:
		model = Devices
		fields = ('Name','IP','Category','Project','Site')
		widgets = {
		'Name': forms.Textarea(attrs={'rows':1}),
		'IP': forms.Textarea(attrs={'rows':1})
		}

class circuit_form(forms.ModelForm):
	class Meta:
		model = Circuit
		fields = ('CircuitID','Bandwidth','WANIP', 'CircuitType', 'Project', 'Site')
		widgets = {
		'CircuitID': forms.Textarea(attrs={'rows':1}),
		'Bandwidth': forms.Textarea(attrs={'rows':1}),
		'WANIP': forms.Textarea(attrs={'rows':1}),
		}
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['Site'].queryset = Circuit.objects.none()
		print(self.data)
		if 'Project' in self.data:
			try:
				Project_id = int(self.data.get('Project'))
				self.fields['Site'].queryset = Sites.objects.filter(Project_id=Project_id).order_by('Name')
			except (ValueError, TypeError):
				pass  # invalid input from the client; ignore and fallback to empty City queryset
		elif self.instance.pk:
			self.fields['Site'].queryset = self.instance.Project.Site_set.order_by('Name')

class edit_circuit_form(forms.ModelForm):
	class Meta:
		model = Circuit
		fields = ('CircuitID','Bandwidth','WANIP', 'CircuitType', 'Project', 'Site')
		widgets = {
		'CircuitID': forms.Textarea(attrs={'rows':1}),
		'Bandwidth': forms.Textarea(attrs={'rows':1}),
		'WANIP': forms.Textarea(attrs={'rows':1}),
		}

class project_form(forms.ModelForm):
	class Meta:
		model = Projects
		fields = ('Name','StartDate','EndDate')
		widgets = {
		'Name': forms.Textarea(attrs={'rows':2}),
		'StartDate': forms.Textarea(attrs={'rows':2}),
		'EndDate': forms.Textarea(attrs={'rows':2})
		}

		#help_texts = {
		#	'StartDate':('(dd/mm/yyyy)'),
		#	'EndDate':('(dd/mm/yyyy)'),
		#}