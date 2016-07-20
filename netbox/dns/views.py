from django_tables2 import RequestConfig

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from ipam.models import IPAddress
from utilities.paginator import EnhancedPaginator
from utilities.views import (
	BulkDeleteView, BulkEditView, BulkImportView, ObjectDeleteView, ObjectEditView, ObjectListView,
)

from . import filters, forms, tables
from .models import Zone, Record

#
# Zones
#

class ZoneListView(ObjectListView):
	queryset = Zone.objects.annotate(record_count=Count('records'))
	filter = filters.ZoneFilter
	filter_form = forms.ZoneFilterForm
	table = tables.ZoneTable
	edit_permissions = ['dns.change_zone', 'dns.delete_zone']
	template_name = 'dns/zone_list.html'

def zone(request, pk):

	zone = get_object_or_404(Zone.objects.all(), pk=pk)
	records = Record.objects.filter(zone=zone)
	record_count = len(records)

	return render(request, 'dns/zone.html', {
		'zone': zone,
		'records': records,
		'record_count': record_count,
	})

class ZoneEditView(PermissionRequiredMixin, ObjectEditView):
	permission_required = 'dns.change_zone'
	model = Zone
	form_class = forms.ZoneForm
	cancel_url = 'dns:zone_list'

class ZoneDeleteView(PermissionRequiredMixin, ObjectDeleteView):
	permission_required = 'dns.delete_zone'
	model = Zone
	redirect_url = 'dns:zone_list'


class ZoneBulkImportView(PermissionRequiredMixin, BulkImportView):
	permission_required = 'dns.add_zone'
	form = forms.ZoneImportForm
	table = tables.ZoneTable
	template_name = 'dns/zone_import.html'
	obj_list_url = 'dns:zone_list'

class ZoneBulkEditView(PermissionRequiredMixin, BulkEditView):
	permission_required = 'dns.change_zone'
	cls = Zone
	form = forms.ZoneBulkEditForm
	template_name = 'dns/zone_bulk_edit.html'
	default_redirect_url = 'dns:zone_list'

	def update_objects(self, pk_list, form):

		fields_to_update = {}
		for field in ['name', 'ttl', 'soa_name', 'soa_contact', 'soa_refresh', 'soa_retry', 'soa_expire', 'soa_minimum']:
			if form.cleaned_data[field]:
				fields_to_update[field] = form.cleaned_data[field]

		return self.cls.objects.filter(pk__in=pk_list).update(**fields_to_update)


class ZoneBulkDeleteView(PermissionRequiredMixin, BulkDeleteView):
    permission_required = 'dns.delete_zone'
    cls = Zone
    form = forms.ZoneBulkDeleteForm
    default_redirect_url = 'dns:zone_list'

#
# Records
#

class RecordListView(ObjectListView):
	queryset = Record.objects.all()
	filter = filters.RecordFilter
	filter_form = forms.RecordFilterForm
	table = tables.RecordTable
	edit_permissions = ['dns.change_record', 'dns.delete_record']
	template_name = 'dns/record_list.html'

def record(request, pk):

	record = get_object_or_404(Record.objects.all(), pk=pk)

	return render(request, 'dns/record.html', {
		'record': record,
	})

class RecordEditView(PermissionRequiredMixin, ObjectEditView):
	permission_required = 'dns.change_record'
	model = Record
	form_class = forms.RecordForm
	cancel_url = 'dns:record_list'

class RecordDeleteView(PermissionRequiredMixin, ObjectDeleteView):
	permission_required = 'dns.delete_record'
	model = Record
	redirect_url = 'dns:record_list'

class RecordBulkImportView(PermissionRequiredMixin, BulkImportView):
	permission_required = 'dns.add_record'
	form = forms.RecordImportForm
	table = tables.RecordTable
	template_name = 'dns/record_import.html'
	obj_list_url = 'dns:record_list'

class RecordBulkEditView(PermissionRequiredMixin, BulkEditView):
	permission_required = 'dns.change_record'
	cls = Record
	form = forms.RecordBulkEditForm
	template_name = 'dns/record_bulk_edit.html'
	default_redirect_url = 'dns:record_list'

	def update_objects(self, pk_list, form):

		fields_to_update = {}
		for field in ['name', 'record_type', 'priority', 'zone', 'address', 'value']:
			if form.cleaned_data[field]:
				fields_to_update[field] = form.cleaned_data[field]

		return self.cls.objects.filter(pk__in=pk_list).update(**fields_to_update)

class RecordBulkDeleteView(PermissionRequiredMixin, BulkDeleteView):
	permission_required = 'dns.delete_record'
	cls = Record
	form = forms.RecordBulkEditForm
	default_redirect_url = 'dns:record_list'
