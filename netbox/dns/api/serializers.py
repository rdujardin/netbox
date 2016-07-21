from rest_framework import serializers

from ipam.api.serializers import IPAddressNestedSerializer
from dns.models import Zone, Record

#
# Zones
#

class ZoneSerializer(serializers.ModelSerializer):

	bind_export = serializers.SerializerMethodField()

	class Meta:
		model=Zone
		fields = ['id', 'name', 'ttl', 'soa_name', 'soa_contact', 'soa_serial', 'soa_refresh', 'soa_retry', 'soa_expire', 'soa_minimum']

	def get_bind_export(self, obj):
		records = Record.objects.filter(zone=obj)
		return {
			'export': obj.to_bind(records),
		}

class ZoneNestedSerializer(ZoneSerializer):

	class Meta(ZoneSerializer.Meta):
		fields = ['id', 'name']


#
# Records
#

class RecordSerializer(serializers.ModelSerializer):

	zone = ZoneNestedSerializer()
	address = IPAddressNestedSerializer()
	bind_export = serializers.SerializerMethodField()

	class Meta:
		model=Record
		fields = ['id', 'name', 'record_type', 'priority', 'zone', 'address', 'value']

	def get_bind_export(self, obj):
		return {
			'export': obj.to_bind(),
		}

class RecordNestedSerializer(RecordSerializer):

	class Meta(RecordSerializer.Meta):
		fields = ['id', 'name', 'record_type', 'zone']