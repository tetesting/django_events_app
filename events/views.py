from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView

from django.contrib import messages

from .models import Event, User
from events import forms
from .view_helpers import SaveViewWithMessageMixin


class AboutView(generic.TemplateView):
    template_name='events/pages/about.html'


def index_action(request):
    if not request.user.is_authenticated():
        return IndexAnonymousView.as_view()(request)
    return IndexAuthenticatedView.as_view()(request)


class IndexAnonymousView(generic.ListView):
    template_name = 'events/anonymous_index.html'

    def get_queryset(self):
        """"Return the soonest upcoming events."""
        return Event.objects.filter(
                start_date__gte=timezone.now()
            ).order_by('start_date')[:10]


class IndexAuthenticatedView(generic.ListView):
    template_name = 'events/authenticated_index.html'

    def get_queryset(self):
        """"Return the soonest upcoming events that the user RSVP'd to."""
        # print(User.objects.get(pk=self.request.user.id).events_attendees_set.filter(start_date__gte=timezone.now()).query)
        return User.objects.get(pk=self.request.user.id).events_attendees_set.filter(start_date__gte=timezone.now()).order_by('start_date')[:10]


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


class CreateEventView(generic.edit.CreateView):
    form_class = forms.CreateEventForm
    template_name = 'events/event_create.html'
    success_url = '/'

    @method_decorator(login_required(redirect_field_name=''))
    def dispatch(self, *args, **kwargs):
        return super(CreateEventView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.organizer_id = self.request.user.id
        self.object.save()
        form.save_m2m()

        # organizer of event attends event by default
        self.object.attendees.add(self.request.user.id)

        return HttpResponseRedirect(self.get_success_url())


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



class UserPasswordChangeView(
            SaveViewWithMessageMixin, generic.edit.UpdateView):
    model = User
    template_name = 'events/user_password_change.html'
    form_class = forms.UserPasswordChangeForm
    success_url = '/user-settings/'

    def get_object(self):
        return User.objects.get(pk=self.request.user.id)

    @method_decorator(login_required(redirect_field_name=''))
    def dispatch(self, *args, **kwargs):
        return super(UserPasswordChangeView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        message_dict = { 
            'success' : 'Your password has been changed.',
            'error' : 'Your password was not changed ' +
                        'due to the errors listed below.' }
        return super(UserPasswordChangeView, self).post(
                        request, message_dict, *args, **kwargs)
        

class UserSettingsView(
            SaveViewWithMessageMixin, generic.edit.UpdateView):
    model = User
    template_name = 'events/user_settings.html'
    form_class = forms.UserSettingsForm
    success_url = '/user-settings/'
    
    def get_object(self):
        return User.objects.get(pk=self.request.user.id)

    @method_decorator(login_required(redirect_field_name=''))
    def dispatch(self, *args, **kwargs):
        return super(UserSettingsView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        message_dict = { 
            'success' : 'Profile details updated.',
            'error' : 'Profile details remain unchanged ' +
                        'Please fix the errors below first.' }
        return super(UserSettingsView, self).post(
                        request, message_dict, *args, **kwargs)



