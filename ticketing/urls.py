from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('ticketing.views',

    url(r'^my-tickets/$', 'my_tickets', name='my_tickets'),
    url(r'^create-raffle/$', 'create_raffle', name='create_raffle'),
    url(r'^view-product/(?P<product_id>\d+)$', 'view_product', name='view_product'),

    url(r'^purchase/(?P<product_id>\d+)$', 'purchase', name='purchase'),

)
