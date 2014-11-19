from django.conf.urls import patterns, include, url
from registration.forms import LoginForm, ResetPWord


urlpatterns = patterns('',

    #registration
    url(r'^$', 'registration.views.register', name='register'),
    url(r'^login/$', 'django.contrib.auth.views.login', kwargs={'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', kwargs={'next_page': '/'}, name='logout'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', kwargs={'password_reset_form': ResetPWord}, name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

    # url(r'^upload_profile_picture/$', 'registration.views.upload_profile_picture', name='upload_profile_picture'),
    # url(r'^new-social-user-redirect', 'registration.views.new_social_user_redirect', name='new-social-user-redirect'),

    # url(r'^ajax-about-me-update/$', 'registration.views.ajax_about_me_update', name='ajax_about_me_update'),
)