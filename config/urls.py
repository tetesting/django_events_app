from django.conf.urls import patterns, include, url

import events.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_events_app.views.home', name='home'),
    # url(r'^django_events_app/', include('django_events_app.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),


    # url(r'^events/', include('events.urls', namespace='events')),

    url(r'^$', events.views.IndexView.as_view(), name='index'),
    url(r'^about/$', events.views.AboutView.as_view(), name='about'),
    url(r'^upcoming-events/$', events.views.UpcomingEventsView.as_view(), name='upcoming_events'),
    url(r'^past-events/$', events.views.PastEventsView.as_view(), name='past_events'),
    url(r'^(?P<pk>\d+)/$', events.views.DetailView.as_view(), name='detail'),
    url(r'^login/$', events.views.LoginView.as_view(), name='login'),
    url(r'^register/$', events.views.register_action, name='register'),
    url(r'^logout/$', events.views.logout_action, name='logout'),
    url(r'^user-settings/$', events.views.UserSettingsView.as_view(), name='user_settings'),
)
