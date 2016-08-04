import os
import time
from django.dispatch import Signal


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
    mod = __import__('userscripts.%s' % name)


def _load():
    scripts = os.listdir('userscripts')
    for script in scripts:
        script = script.lower()
        if script.endswith('.py') and script != '__init__.py':
            script = script[:-3]
            _load_script(script)
