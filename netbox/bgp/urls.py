from django.conf.urls import url

from . import views

urlpatterns = [

    # ASNs
    url(r'^asns/$', views.ASNListView.as_view(), name='asn_list'),
    url(r'^asns/add/$', views.ASNEditView.as_view(), name='asn_add'),
    url(r'^asns/import/$', views.ASNBulkImportView.as_view(), name='asn_import'),
    url(r'^asns/edit/$', views.ASNBulkEditView.as_view(), name='asn_bulk_edit'),
    url(r'^asns/delete/$', views.ASNBulkDeleteView.as_view(), name='asn_bulk_delete'),
    url(r'^asn/(?P<asn>\d+)/$', views.asn, name='asn'),
    url(r'^asn/(?P<asn>\d+)/edit/$', views.ASNEditView.as_view(), name='asn_edit'),
    url(r'^asn/(?P<asn>\d+)/delete/$', views.ASNDeleteView.as_view(), name='asn_delete'),

]