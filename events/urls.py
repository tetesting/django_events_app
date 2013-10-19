from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

import events.views

urlpatterns = patterns('',
    url(r'^$', events.views.index_action, name='index'),
    url(r'^about/$', events.views.AboutView.as_view(), name='about'),
    url(r'^upcoming-events/$', events.views.UpcomingEventsView.as_view(), name='upcoming_events'),
    url(r'^past-events/$', events.views.PastEventsView.as_view(), name='past_events'),
    url(r'^(?P<pk>\d+)/$', events.views.DetailView.as_view(), name='detail'),
    url(r'^login/$', never_cache(events.views.LoginView.as_view()), name='login'),
    url(r'^register/$', events.views.RegisterView.as_view(), name='register'),
    url(r'^logout/$', events.views.logout_action, name='logout'),
    url(r'^user-settings/$', never_cache(events.views.UserSettingsView.as_view()), name='user_settings'),
    url(r'^change-password/$', never_cache(events.views.UserPasswordChangeView.as_view()), name='user_password_change'),

    url(r"^robots\.txt$", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
)
