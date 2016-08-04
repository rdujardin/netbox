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
    logger = logging.getLogger(__name__)
    logger.info('! Request')


@receiver(pre_save, sender=IPAddress)
def callback_ipaddress_pre_save(sender, **kwargs):
    logger = logging.getLogger(__name__)
    logger.info('! IP Pre-save')
