from django.conf.urls import patterns, include, url

from events import views as events_views

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

    url(r'^$', events_views.IndexView.as_view(), name='index'),
    url(r'^about/$', events_views.AboutView.as_view(), name='about'),
    url(r'^upcoming-events/$', events_views.UpcomingEventsView.as_view(), name='upcoming_events'),
    url(r'^past-events/$', events_views.PastEventsView.as_view(), name='past_events'),
    url(r'^(?P<pk>\d+)/$', events_views.DetailView.as_view(), name='detail'),
)
