from django.core.urlresolvers import reverse
from django.db import models

from utilities.models import CreatedUpdatedModel
from utilities.whois import whois

import subprocess
import json


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

    def save(self, *args, **kwargs):
        self.load_data()
        super(ASN, self).save(*args, **kwargs)

    def load_data(self):
        self_ixp_asn = 51706
        who = whois('rr.ntt.net', 'AS{}'.format(self.asn))
        if not who:
            return
        self.as_name = who['as-name'][0] if 'as-name' in who else self.as_name

        if not self.lock_as_set:
            ln_export = who['export'] if 'export' in who else []
            ln_export_via = who['export-via'] if 'export-via' in who else []
            ln_mp_export = who['mp-export'] if 'mp-export' in who else []
            ios = ln_export + ln_export_via + ln_mp_export
            for io in ios:
                if 'AS{}'.format(self_ixp_asn) in io:
                    as_set = io.split('announce')
                    if as_set:
                        as_set = as_set[len(as_set) - 1].strip()
                        if 'ipv4' in io and not 'ipv6' in io:
                            self.as_set4 = as_set
                        elif 'ipv6' in io and not 'ipv4' in io:
                            self.as_set6 = as_set
                        else:
                            self.as_set4 = as_set
                            self.as_set6 = as_set

            bgpq3_queries_v4 = (
                self.as_set4 if self.as_set4 else None,
                'AS{}'.format(self.asn) if not self.as_set4 else None,
            )

            bgpq3_queries_v6 = (
                self.as_set6 if self.as_set6 and self.as_set4 else None,
                'AS{}'.format(self.asn) if not self.as_set4 else None,
            )

            for q in bgpq3_queries_v4:
                if q:
                    cmd = ['bgpq3', '-h', 'rr.ntt.net', '-S', 'RIPE,APNIC,AFRINIC,ARIN,NTTCOM,ALTDB,BBOI,BELL,GT,JPIRR,LEVEL3,RADB,RGNET,SAVVIS,TC', '-A', '-j', '-l', 'data', q]
                    try:
                        bgpq3 = json.loads(subprocess.check_output(cmd))
                        prefixes = []
                        for p in bgpq3['data']:
                            prefixes.append(p['prefix'])
                        self.prefixes4 = ';'.join(prefixes)
                    except:
                        return

            for q in bgpq3_queries_v6:
                if q:
                    cmd = ['bgpq3', '-h', 'rr.ntt.net', '-S', 'RIPE,APNIC,AFRINIC,ARIN,NTTCOM,ALTDB,BBOI,BELL,GT,JPIRR,LEVEL3,RADB,RGNET,SAVVIS,TC', '-A', '-j', '-6', '-l', 'data', q]
                    try:
                        bgpq3 = json.loads(subprocess.check_output(cmd))
                        prefixes = []
                        for p in bgpq3['data']:
                            prefixes.append(p['prefix'])
                        self.prefixes6 = ';'.join(prefixes)
                    except:
                        return














