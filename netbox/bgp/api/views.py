from rest_framework import generics
from bgp.models import ASN
from . import serializers


#
# ASNs
#

class ASNListView(generics.ListAPIView):
    """
    List all ASNs
    """
    queryset = ASN.objects.select_related('tenant')
    serializer_class = serializers.ASNSerializer


class ASNDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single ASN
    """
    queryset = ASN.objects.select_related('tenant')
    serializer_class = serializers.ASNSerializer
