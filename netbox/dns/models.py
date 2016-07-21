
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models

from ipam.models import IPAddress
from utilities.models import CreatedUpdatedModel

import time

class Zone(CreatedUpdatedModel):
	"""
	A Zone represents a DNS zone. It contains SOA data but no records, records are represented as Record objects.
	"""
	name=models.CharField(max_length=100)
	ttl=models.PositiveIntegerField()
	soa_name=models.CharField(max_length=100)
	soa_contact=models.CharField(max_length=100)
	soa_serial=models.CharField(max_length=100)
	soa_refresh=models.PositiveIntegerField()
	soa_retry=models.PositiveIntegerField()
	soa_expire=models.PositiveIntegerField()
	soa_minimum=models.PositiveIntegerField()

	class Meta:
		ordering = ['name']

	def __unicode__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('dns:zone', args=[self.pk])

	def to_csv(self):
		return ','.join([
			self.name,
			str(self.ttl),
			self.soa_name,
			self.soa_contact,
			self.soa_serial,
			str(self.soa_refresh),
			str(self.soa_retry),
			str(self.soa_expire),
			str(self.soa_minimum),
		])

	def to_bind(self,records):
		bind_records = ''
		for r in records:
			bind_records += r.to_bind()+'\n'
		bind_export = '\n'.join([
			'; gen by netbox ( '+time.strftime('%A %B %d %Y %H:%M:%S',time.localtime())+' ) ',
			'',
			'$TTL '+str(self.ttl),
			self.soa_name.ljust(30)+'    IN    '+'SOA                   '+self.soa_contact+' (',
			'    '+self.soa_serial.ljust(30)+' ; serial',
			'    '+str(self.soa_refresh).ljust(30)+' ; refresh',
			'    '+str(self.soa_retry).ljust(30)+' ; retry',
			'    '+str(self.soa_expire).ljust(30)+' ; expire',
			'    '+str(self.soa_minimum).ljust(29)+') ; minimum',
			'',
			'',
			'',
		])
		bind_export += '\n'+bind_records
		bind_export += '\n'+'; end '
		return bind_export



class Record(CreatedUpdatedModel):
	"""
	A Record represents a DNS record, i.e. a row in a DNS zone.
	"""
	name=models.CharField(max_length=100)
	record_type=models.CharField(max_length=10)
	priority=models.PositiveIntegerField(blank=True, null=True)
	zone=models.ForeignKey('Zone', related_name='records', on_delete=models.CASCADE)
	address=models.ForeignKey('ipam.IPAddress', related_name='records', on_delete=models.SET_NULL, blank=True, null=True)
	value=models.CharField(max_length=100, blank=True)

	class Meta:
		ordering = ['name']

	def __unicode__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('dns:record', args=[self.pk])

	def clean(self):
		record_type = record_type.upper()
		if not self.address and not self.value:
			raise ValidationError("DNS records must have either an IP address or a text value")

	def to_csv(self):
		return ','.join([
			self.zone.name,
			self.name,
			self.record_type,
			str(self.priority) if self.priority else '',
			str(self.address) if self.address else '',
			str(self.value) if self.value else '',
		])

	def to_bind(self):
		return ''.join([
			(self.name if self.name!='@' else '').ljust(30),
			'    IN    ',
			self.record_type.upper().ljust(10),
			'    ',
			(str(self.priority) if self.priority else '').ljust(4),
			'    ',
			(str(self.address).split('/')[0] if self.address else self.value).ljust(25),
			'  ',
			' ; gen by netbox ( '+time.strftime('%A %B %d %Y %H:%M:%S',time.localtime())+' ) '
		])


