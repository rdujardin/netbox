from django.core.signals import request_finished
from django.db.models.signals import pre_save
from django.dispatch import receiver
from userscripts import pre_bulk_edit, post_bulk_edit

from circuits.models import Provider
from ipam.models import IPAddress

import time
import logging


@receiver(request_finished)
def callback_request_finished(sender, **kwargs):
    logger = logging.getLogger('example.py')
    logger.info('! Request')


@receiver(pre_save, sender=IPAddress)
def callback_ipaddress_pre_save(sender, **kwargs):
    logger = logging.getLogger('example.py')
    logger.info('! IP Pre-save')

@receiver(pre_bulk_edit, sender=Provider)
def callback_ipaddress_pre_bulk_edit(sender, **kwargs):
    msg = '! Provider Pre-bulk-edit ('
    for pk in kwargs['pk_list']:
        msg += pk + ','
    msg += ')'
    logger = logging.getLogger('example.py')
    logger.info(msg)

@receiver(pre_bulk_edit)
def callback_pre_bulk_edit(sender, **kwargs):
    msg = '! {} Pre-bulk-edit ('.format(str(sender))
    for pk in kwargs['pk_list']:
        msg += pk + ','
    msg += ')'
    logger = logging.getLogger('example.py')
    logger.info(msg)

def call(**kwargs):
    logger = logging.getLogger('example.py')
    response = 'Hello {}.'.format(name if name else 'folk')
    logger.info('Called, response : {}'.format(response))
    return response
    
