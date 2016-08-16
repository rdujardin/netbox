import django_tables2 as tables
from django_tables2.utils import Accessor

from utilities.tables import BaseTable, ToggleColumn

from .models import ASN


#
# ASNs
#

class ASNTable(BaseTable):
    pk = ToggleColumn()
    asn = tables.LinkColumn('bgp:asn', args=[Accessor('asn')])
    tenant = tables.LinkColumn('tenancy:tenant', args=[Accessor('slug')])

    class Meta(BaseTable.Meta):
        model = ASN
        fields = ('pk', 'asn', 'tenant', 'as_name', 'as_set4', 'as_set6', 'lock_as_set')