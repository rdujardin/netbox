import os
import time
from django.dispatch import Signal
import logging
from logging.handlers import RotatingFileHandler
import netbox.configuration
import importlib


pre_bulk_edit = Signal(providing_args=['pk_list'])
post_bulk_edit = Signal(providing_args=['pk_list'])


class signal_bulk_edit:
    def __init__(self, cls, pk_list):
        self.cls = cls
        self.pk_list = pk_list

    def __enter__(self):
        return pre_bulk_edit.send(sender=self.cls, pk_list=self.pk_list)

    def __exit__(self, type, value, traceback):
        return post_bulk_edit.send(sender=self.cls, pk_list=self.pk_list)


def _load_script(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    log_formatter = logging.Formatter('--------------------------------------------------\n%(asctime)s - {} - %(levelname)s\n-------------------------\n%(message)s\n--------------------------------------------------\n'.format(name))
    log_handler = RotatingFileHandler(netbox.configuration.USERSCRIPTS_LOG_FILE if netbox.configuration.USERSCRIPTS_LOG_FILE else 'userscripts.log', 'a', netbox.configuration.USERSCRIPTS_LOG_MAX_SIZE if netbox.configuration.USERSCRIPTS_LOG_MAX_SIZE else 5000000, 1)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(log_formatter)
    log.addHandler(log_handler)
    mod = importlib.import_module('userscripts.%s' % name)


def _load():
    scripts = os.listdir('userscripts')
    for script in scripts:
        script = script.lower()
        if script.endswith('.py') and script != '__init__.py':
            script = script[:-3]
            _load_script(script)
