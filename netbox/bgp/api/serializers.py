from rest_framework import serializers

from bgp.models import ASN


#
# ASNs
#

class ASNSerializer(serializers.ModelSerializer):
    class Meta:
        model = ASN
        fields = ['id', 'asn', 'as_name', 'tenant', 'as_set4', 'as_set6', 'lock_as_set', 'prefixes4', 'prefixes6']


class ASNNestedSerializer(ASNSerializer):
    class Meta(ASNSerializer.Meta):
        fields = ['id', 'asn', 'as_name', 'tenant']
