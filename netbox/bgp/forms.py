from django import forms
from django.db.models import Count

from utilities.forms import (
    BootstrapMixin, BulkImportForm, CommentField, CSVDataField, SlugField,
)

from .models import ASN
from tenancy.models import Tenant


#
# ASNs
#


class ASNForm(forms.ModelForm, BootstrapMixin):

    class Meta:
        model = ASN
        fields = ['asn', 'tenant', 'as_name', 'as_set4', 'as_set6', 'lock_as_set', 'prefixes4', 'prefixes6']


class ASNFromCSVForm(forms.ModelForm):
    tenant = forms.ModelChoiceField(Tenant.objects.all(), to_field_name='name', required=False,
                                    error_messages={'invalid_choice': 'Tenant not found.'})

    class Meta:
        model = ASN
        fields = ['asn', 'as_name', 'tenant', 'as_set4', 'as_set6', 'lock_as_set', 'prefixes4', 'prefixes6']


class ASNImportForm(BulkImportForm, BootstrapMixin):
    csv = CSVDataField(csv_form=ASNFromCSVForm)


class ASNBulkEditForm(forms.Form, BootstrapMixin):
    asn = forms.IntegerField(required=False)
    as_name = forms.CharField(max_length=100, required=False)
    tenant = forms.ModelChoiceField(queryset=Tenant.objects.all(), required=False)
    as_set4 = forms.CharField(max_length=100, required=False)
    as_set6 = forms.CharField(max_length=100, required=False)
    lock_as_set = forms.BooleanField(required=False)
    prefixes4 = forms.CharField(required=False)
    prefixes6 = forms.CharField(required=False)


def tenant_choices():
    tenant_choices = Tenant.objects.annotate(tenant_count=Count('name'))
    return [(t.name, u'{} ({})'.format(t.name, t.tenant_count)) for t in tenant_choices]


class ASNFilterForm(forms.Form, BootstrapMixin):
    tenant = forms.MultipleChoiceField(required=False, choices=tenant_choices,
                                       widget=forms.SelectMultiple(attrs={'size': 8}))