import django_filters

from ipam.models import IPAddress
from .models import (
	Zone,
	Record,
)

class ZoneFilter(django_filters.FilterSet):
	name = django_filters.CharFilter(
		name='name',
		lookup_type='icontains',
		label='Name',
	)

	class Meta:
		model = Zone
		fields = ['name']

class RecordFilter(django_filters.FilterSet):
	zone__name = django_filters.ModelMultipleChoiceFilter(
		name='zone__name',
		to_field_name='name',
		lookup_type='icontains',
		queryset=Zone.objects.all(),
		label='Zone (name)',
	)
	name = django_filters.CharFilter(
		name='name',
		lookup_type='icontains',
		label='Name',
	)

	class Meta:
		model=Record
		field = ['name','record_type','value']
