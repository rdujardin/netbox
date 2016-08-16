import django_filters

from tenancy.models import Tenant
from .models import ASN


class ASNFilter(django_filters.FilterSet):

    tenant = django_filters.ModelMultipleChoiceFilter(
        name='tenant',
        queryset=Tenant.objects.all(),
        to_field_name='name',
        label='Tenant (name)',
    )

    class Meta:
        model = ASN
        fields = ['tenant']