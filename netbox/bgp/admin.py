from django.contrib import admin

from .models import ASN


@admin.register(ASN)
class ASNAdmin(admin.ModelAdmin):
    list_display = ['asn', 'tenant', 'as_name', 'as_set4', 'as_set6', 'lock_as_set']