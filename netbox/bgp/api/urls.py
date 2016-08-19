from django.conf.urls import url
from .views import *


urlpatterns = [

    # ASNs
    url(r'^asns/$', ASNListView.as_view(), name='asn_list'),
    url(r'^asns/(?P<asn>\d+)/$', ASNDetailView.as_view(), name='asn_detail'),

]
