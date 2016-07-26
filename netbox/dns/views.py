from django_tables2 import RequestConfig

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from ipam.models import IPAddress, Prefix
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
	bind_export = zone.to_bind(records)

	if request.GET.get('bind_export'):
		response = HttpResponse(
			bind_export,
			content_type='text/plain'
		)
		response['Content-Disposition'] = 'attachment; filename="netbox_{}.txt"'\
			.format(zone.name)
		return response

	else: 
		return render(request, 'dns/zone.html', {
			'zone': zone,
			'records': records,
			'record_count': record_count,
			'bind_export': bind_export,
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

		zlist = self.cls.objects.filter(pk__in=pk_list)
		for z in zlist:
			z.save()
		return zlist.update(**fields_to_update)


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
	bind_export = record.to_bind()

	return render(request, 'dns/record.html', {
		'record': record,
		'bind_export': bind_export,
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

		rlist = self.cls.objects.filter(pk__in=pk_list)
		if rlist:
			rlist[0].save()
		return rlist.update(**fields_to_update)

class RecordBulkDeleteView(PermissionRequiredMixin, BulkDeleteView):
	permission_required = 'dns.delete_record'
	cls = Record
	form = forms.RecordBulkEditForm
	default_redirect_url = 'dns:record_list'

#
# Full Reverse
#

def full_reverse(request):

	zones = {}

	prefixes = Prefix.objects.all()

	for p in prefixes:
		child_ip = IPAddress.objects.filter(address__net_contained_or_equal=str(p.prefix))
		z = p.to_bind(child_ip)
		for zz in z:
			if not zz['id'] in zones:
				zones[zz['id']] = zz['content']

	zones_list = []
	for zid,zc in zones.items():
		zones_list.append({
			'num': len(zones_list),
			'id': zid,
			'content': zc,
		})

	return render(request, 'dns/full_reverse.html', {
		'zones': zones_list,
		'bind_export_count': len(zones_list),
	})
