from django import forms
from django.db.models import Count

from ipam.models import IPAddress
from utilities.forms import (
	BootstrapMixin, ConfirmationForm, APISelect, Livesearch, CSVDataField, BulkImportForm,
)

from .models import (
	Zone,
	Record,
)

#
# Zones
#

class ZoneForm(forms.ModelForm, BootstrapMixin):

	class Meta:
		model=Zone
		fields = ['name', 'ttl', 'soa_name', 'soa_contact', 'soa_serial', 'soa_refresh', 'soa_retry', 'soa_expire', 'soa_minimum']
		labels = {
			'soa_name': 'SOA Name',
			'soa_contact': 'SOA Contact',
			'soa_serial': 'SOA Serial',
			'soa_refresh': 'SOA Refresh',
			'soa_retry': 'SOA Retry',
			'soa_expire': 'SOA Expire',
			'soa_minimum': 'SOA Minimum',
		}

class ZoneFromCSVForm(forms.ModelForm):

	class Meta:
		model=Zone
		fields = ['name', 'ttl', 'soa_name', 'soa_contact', 'soa_serial', 'soa_refresh', 'soa_retry', 'soa_expire', 'soa_minimum']

class ZoneImportForm(BulkImportForm, BootstrapMixin):
	csv = CSVDataField(csv_form=ZoneFromCSVForm)

class ZoneBulkEditForm(forms.Form, BootstrapMixin):
	pk = forms.ModelMultipleChoiceField(queryset=Zone.objects.all(), widget=forms.MultipleHiddenInput)
	name = forms.CharField(max_length=100, required=False, label='Name')
	ttl = forms.IntegerField(required=False, label='TTL')
	soa_name = forms.CharField(max_length=100, required=False, label='SOA Name')
	soa_contact = forms.CharField(max_length=100, required=False, label='SOA Contact')
	soa_refresh = forms.IntegerField(required=False, label='SOA Refresh')
	soa_retry = forms.IntegerField(required=False, label='SOA Retry')
	soa_expire = forms.IntegerField(required=False, label='SOA Expire')
	soa_minimum = forms.IntegerField(required=False, label='SOA Minimum')


class ZoneBulkDeleteForm(ConfirmationForm):
	pk = forms.ModelMultipleChoiceField(queryset=Zone.objects.all(), widget=forms.MultipleHiddenInput)

class ZoneFilterForm(forms.Form, BootstrapMixin):
	pass

#
# Records
#

class RecordForm(forms.ModelForm, BootstrapMixin):

	class Meta:
		model=Record
		fields = ['name', 'record_type', 'priority', 'zone', 'address', 'value']
		labels = {
			'record_type': 'Type',
		}

class RecordFromCSVForm(forms.ModelForm):

	zone = forms.ModelChoiceField(queryset=Zone.objects.all(), to_field_name='name', error_messages={'invalid_choice': 'Zone not found.'})
	address = forms.ModelChoiceField(queryset=IPAddress.objects.all(), to_field_name='address', error_messages={'invalid_choice': 'IP Address not found.'}, required=False)

	class Meta:
		model=Record
		fields = ['zone', 'name', 'record_type', 'priority', 'address', 'value']

class RecordImportForm(BulkImportForm, BootstrapMixin):
	csv = CSVDataField(csv_form=RecordFromCSVForm)

class RecordBulkEditForm(forms.Form, BootstrapMixin):
	pk = forms.ModelMultipleChoiceField(queryset=Record.objects.all(), widget=forms.MultipleHiddenInput)
	name = forms.CharField(max_length=100, required=False, label='Name')
	record_type = forms.CharField(max_length=100, required=False, label='Type')
	priority = forms.IntegerField(required=False)
	zone = forms.ModelChoiceField(queryset=Zone.objects.all(), required=False)
	address = forms.ModelChoiceField(queryset=IPAddress.objects.all(), required=False)
	value = forms.CharField(max_length=100, required=False)

class RecordBulkDeleteForm(ConfirmationForm):
	pk = forms.ModelMultipleChoiceField(queryset=Record.objects.all(), widget=forms.MultipleHiddenInput)

def record_zone_choices():
	zone_choices = Zone.objects.annotate(record_count=Count('records'))
	return [(z.name, '{} ({})'.format(z.name, z.record_count)) for z in zone_choices]

#def record_name_choices():
	#name_choices = 

class RecordFilterForm(forms.Form, BootstrapMixin):
	zone__name = forms.MultipleChoiceField(required=False, choices=record_zone_choices, label='Zone',
										widget=forms.SelectMultiple(attrs={'size': 8}))
	#name = forms.MultipleChoiceField(required=False, choices=record_name_choices, label='Name', widget=forms.SelectMultiple(attrs={'size': 8}))
	record_type = forms.CharField(max_length=100, required=False, label='Type')

