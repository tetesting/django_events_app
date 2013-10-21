from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout

from django.views.generic.edit import FormView

from django.contrib import messages

from .models import Event, User
from events import forms
from .view_helpers import LoginRequiredMixin, SaveViewWithMessageMixin, MyEventsMixin


class AboutView(generic.TemplateView):
    template_name='events/pages/about.html'


def index_action(request):
    if not request.user.is_authenticated():
        return IndexAnonymousView.as_view()(request)
    return IndexAuthenticatedView.as_view()(request)


class IndexAnonymousView(generic.ListView):
    template_name = 'events/anonymous_index.html'
    limit = 10

    def get_queryset(self):
        """"Return the soonest upcoming events."""
        return Event.objects.filter(
                start_date__gte=timezone.now()
            ).order_by('start_date')[:self.limit]


class IndexAuthenticatedView(MyEventsMixin, generic.ListView):
    """
    display:
        6 upcoming events that the user is organizing;
        6 upcoming events that the user is attending;
        6 upcoming events that the user may be interested in;
    """
    template_name = 'events/authenticated_index.html'
    limit = 6

    def get_queryset(self):
        """"Return the soonest upcoming events that the user is not attending."""
        return Event.objects.exclude(
                attendees__id__exact=self.request.user.id
            ).filter(
                start_date__gte=timezone.now()
            ).order_by('start_date')[:self.limit]

    def get_context_data(self, **kwargs):
        context = super(IndexAuthenticatedView, self).get_context_data(**kwargs)

        organizing_list = self.get_events_organizing(self.limit)
        attending_list = self.get_events_attending(self.limit)
        kwargs.update({'organizing_list' : organizing_list})
        kwargs.update({'attending_list' : attending_list})

        context.update(kwargs)
        return context

class DetailView(generic.DetailView):
    model = Event

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        success_url = "/{}/".format(self.object.id)

        if (request.POST['action'] == 'attend'):
            self.object.attendees.add(request.user.id)
        else:
            self.object.attendees.remove(request.user.id)

        return HttpResponseRedirect(success_url)

class PastEventsView(generic.ListView):
    """
    display:
        past events that the user may have been interested in,
        as well as an indicator for their RSVP.
    """
    template_name = 'events/event_list_past.html'
    limit = 10

    def get_queryset(self):
        """"Return the latest past events."""
        return Event.objects.filter(
                start_date__lte=timezone.now()
            ).order_by('-start_date')[:self.limit]


class UpcomingEventsView(generic.ListView):
    """
    display:
        upcoming events that the user may be interested in,
        as well as an indicator for their RSVP.
    """
    template_name = 'events/event_list_upcoming.html'

    def get_queryset(self):
        """"Return the soonest upcoming events."""
        return Event.objects.filter(
                start_date__gte=timezone.now()
            ).order_by('start_date')[:10]


class CreateEventView(LoginRequiredMixin, generic.edit.CreateView):
    form_class = forms.CreateEventForm
    template_name = 'events/event_create.html'
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.organizer_id = self.request.user.id
        self.object.save()
        form.save_m2m()

        # organizer of event attends event by default
        self.object.attendees.add(self.request.user.id)

        return HttpResponseRedirect(self.get_success_url())


class MyEventsView(LoginRequiredMixin, MyEventsMixin, generic.ListView):
    template_name = 'events/my_events.html'
    limit = 10

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        context = super(MyEventsView, self).get_context_data(**kwargs)

        organizing_list = self.get_events_organizing(self.limit)
        attending_list = self.get_events_attending(self.limit)
        kwargs.update({'organizing_list' : organizing_list})
        kwargs.update({'attending_list' : attending_list})

        context.update(kwargs)
        return context

###### Account Stuff


def logout_action(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


class LoginView(generic.edit.CreateView):
    form_class = forms.LoginForm
    template_name = 'events/user_login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        
        form = self.form_class(initial=self.initial)

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')

        form = self.form_class(request.POST)
        username = form.data.get('username')
        password = form.data.get('password')

        if username == '' or password == '':
            return render(request, self.template_name, {'form': form})

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, self.template_name, {'form':form, 
                    'user_is_inactive': True, 'username': username})
        else:
            if 'password' not in form.errors:
                if (User.objects.filter(username=username).count() == 0):
                    error_type = 'not_found'
                else:
                    error_type = 'password'
                context = {'form': form, 
                           'login_error': True, 'error_type': error_type}

            return render(request, self.template_name, context)
    


class RegisterView(
            SaveViewWithMessageMixin, generic.edit.CreateView):
    model = User
    template_name = 'events/user_register.html'
    form_class = forms.RegisterForm
    success_url = '/login/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        self.object = None
        message_dict = { 
            'success' : 'Your account has been successfully created!',
            'error' : 'Your account was not created ' +
                        'due to the errors listed below.' }
        return super(RegisterView, self).post(
                        request, message_dict, *args, **kwargs)



class UserPasswordChangeView(LoginRequiredMixin,
            SaveViewWithMessageMixin, generic.edit.UpdateView):
    model = User
    template_name = 'events/user_password_change.html'
    form_class = forms.UserPasswordChangeForm
    success_url = '/user-settings/'

    def get_object(self):
        return User.objects.get(pk=self.request.user.id)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        message_dict = { 
            'success' : 'Your password has been changed.',
            'error' : 'Your password was not changed ' +
                        'due to the errors listed below.' }
        return super(UserPasswordChangeView, self).post(
                        request, message_dict, *args, **kwargs)
        

class UserSettingsView(LoginRequiredMixin,
            SaveViewWithMessageMixin, generic.edit.UpdateView):
    model = User
    template_name = 'events/user_settings.html'
    form_class = forms.UserSettingsForm
    success_url = '/user-settings/'
    
    def get_object(self):
        return User.objects.get(pk=self.request.user.id)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        message_dict = { 
            'success' : 'Profile details updated.',
            'error' : 'Profile details remain unchanged ' +
                        'Please fix the errors below first.' }
        return super(UserSettingsView, self).post(
                        request, message_dict, *args, **kwargs)



