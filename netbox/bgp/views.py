from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render

from utilities.views import (
    BulkDeleteView, BulkEditView, BulkImportView, ObjectDeleteView, ObjectEditView, ObjectListView,
)

from models import ASN
from . import filters, tables, forms


#
# ASNs
#


class ASNListView(ObjectListView):
    queryset = ASN.objects.all()
    filter = filters.ASNFilter
    filter_form = forms.ASNFilterForm
    table = tables.ASNTable
    edit_permissions = ['bgp.change_asn', 'bgp.delete_asn']
    template_name = 'bgp/asn_list.html'


def asn(request, asn):
    obj_asn = get_object_or_404(ASN, asn=asn)
    return render(request, 'bgp/asn.html', {
        'asn': obj_asn,
    })


class ASNEditView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'bgp.change_asn'
    model = ASN
    form_class = forms.ASNForm
    template_name = 'bgp/asn_edit.html'
    cancel_url = 'bgp:asn_list'


class ASNDeleteView(PermissionRequiredMixin, ObjectDeleteView):
    permission_required = 'bgp.delete_asn'
    model = ASN
    redirect_url = 'bgp:asn_list'


class ASNBulkImportView(PermissionRequiredMixin, BulkImportView):
    permission_required = 'bgp.add_asn'
    form = forms.ASNImportForm
    table = tables.ASNTable
    template_name = 'bgp/asn_import.html'
    obj_list_url = 'bgp:asn_list'


class ASNBulkEditView(PermissionRequiredMixin, BulkEditView):
    permission_required = 'bgp.change_asn'
    cls = ASN
    form = forms.ASNBulkEditForm
    template_name = 'bgp/asn_bulk_edit.html'
    default_redirect_url = 'bgp:asn_list'

    def update_objects(self, pk_list, form):

        fields_to_update = {}
        for field in ['asn', 'as_name', 'tenant', 'as_set4', 'as_set6', 'lock_as_set', 'prefixes4', 'prefixes6']:
            if form.cleaned_data[field]:
                fields_to_update[field] = form.cleaned_data[field]

        objs = self.cls.objects.filter(pk__in=pk_list)
        out = objs.update(**fields_to_update)
        for obj in objs:
            obj.save()
        return out


class ASNBulkDeleteView(PermissionRequiredMixin, BulkDeleteView):
    permission_required = 'bgp.delete_asn'
    cls = ASN
    default_redirect_url = 'bgp:asn_list'