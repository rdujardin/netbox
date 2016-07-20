from rest_framework import generics

from ipam.models import IPAddress
from dns.models import Zone, Record
from dns import filters

from . import serializers

#
# Zones
#

class ZoneListView(generics.ListAPIView):
	"""
	List all zones
	"""
	queryset = Zone.objects.all()
	serializer_class = serializers.ZoneSerializer
	filter_class = filters.ZoneFilter

class ZoneDetailView(generics.RetrieveAPIView):
	"""
	Retrieve a single zone
	"""
	queryset = Zone.objects.all()
	serializer_class = serializers.ZoneSerializer

#
# Records
#

class RecordListView(generics.ListAPIView):
	"""
	List all records
	"""
	queryset = Record.objects.all()
	serializer_class = serializers.RecordSerializer

class RecordDetailView(generics.RetrieveAPIView):
	"""
	Retrieve a single record
	"""
	queryset = Record.objects.all()
	serializer_class = serializers.RecordSerializer
