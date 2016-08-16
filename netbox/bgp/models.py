from django.core.urlresolvers import reverse
from django.db import models

from utilities.models import CreatedUpdatedModel


class ASN(CreatedUpdatedModel):
    """
    An ASN (Autonomous System Number) model stores an AS number and its declarable BGP routes. The model is able to query WHOIS databases to automatically get these routes for the AS and for its AS-SETs.
    """
    asn = models.IntegerField(unique=True, verbose_name='ASN')
    as_name = models.CharField(max_length=100, blank=True, verbose_name='AS Name')
    tenant = models.ForeignKey('tenancy.Tenant', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Tenant')
    as_set4 = models.CharField(max_length=100, blank=True, verbose_name='AS-SET v4')
    as_set6 = models.CharField(max_length=100, blank=True, verbose_name='AS-SET v6')
    lock_as_set = models.BooleanField(default=False, verbose_name='Lock AS-SETs')
    prefixes4 = models.TextField(blank=True, verbose_name='Prefixes v4')
    prefixes6 = models.TextField(blank=True, verbose_name='Prefixes v6')

    class Meta:
        ordering = ['asn']

    def __unicode__(self):
        return 'AS{}'.format(unicode(self.asn))

    def get_absolute_url(self):
        return reverse('bgp:asn', args=[unicode(self.asn)])

    def to_csv(self):
        return ','.join([
            self.asn,
            self.as_name if self.as_name else '',
            self.tenant.name if self.tenant else '',
            self.as_set4 if self.as_set4 else '',
            self.as_set6 if self.as_set6 else '',
            self.lock_as_set,
            self.prefixes4 if self.prefixes4 else '',
            self.prefixes6 if self.prefixes6 else '',
        ])