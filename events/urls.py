from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^upcoming-events/$', views.UpcomingEventsView.as_view(), name='upcoming_events'),
    url(r'^past-events/$', views.PastEventsView.as_view(), name='past_events'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
)
