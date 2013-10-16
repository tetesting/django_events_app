from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Event, User


class AboutView(generic.TemplateView):
    template_name='events/pages/about.html'


class IndexView(generic.ListView):

    def get_queryset(self):
        """"Return the soonest upcoming events."""
        return Event.objects.filter(
                start_date__gte=timezone.now()
            ).order_by('start_date')[:5]


class DetailView(generic.DetailView):
    model = Event


class PastEventsView(generic.ListView):
    template_name = 'events/event_list_past.html'

    def get_queryset(self):
        """"Return the latest past events."""
        return Event.objects.filter(
                start_date__lte=timezone.now()
            ).order_by('-start_date')[:10]


class UpcomingEventsView(generic.ListView):
    template_name = 'events/event_list_upcoming.html'

    def get_queryset(self):
        """"Return the soonest upcoming events."""
        return Event.objects.filter(
                start_date__gte=timezone.now()
            ).order_by('start_date')[:10]



###### Account Stuff


class LoginView(generic.edit.CreateView):
    model = User


class UserSettingsView(generic.edit.UpdateView):
    model = User



def logout(request):
    return HttpResponseRedirect(reverse('index'))




