from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from raffle import settings

urlpatterns = patterns('',
    # Examples:

    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # 3rd Party urls
    url('', include('social.apps.django_app.urls', namespace='social')),


    # raffler urls
    url(r'^$', 'ticketing.views.splash_index', name='splash_index'),

    # Account and Registration Related
    url(r'^account/', 'registration.views.account', name='account'),
    url(r'^registration/', include('registration.urls')),


    # Products Tickets Related
    url(r'^my-products/$', 'ticketing.views.my_products', name='my_products'),
    url(r'^products/$', 'ticketing.views.products', name='products'),
    url(r'^raffle/', include('ticketing.urls')),
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)