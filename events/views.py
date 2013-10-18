from django.http import HttpResponse, HttpResponseRedirect
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


class AboutView(generic.TemplateView):
    template_name='events/pages/about.html'


class IndexView(generic.ListView):

    def get_queryset(self):
        """"Return the soonest upcoming events."""
        return Event.objects.filter(
                start_date__gte=timezone.now()
            ).order_by('start_date')[:5]

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if (self.get_paginate_by(self.object_list) is not None
                and hasattr(self.object_list, 'exists')):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.")
                        % {'class_name': self.__class__.__name__})
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)


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


def logout_action(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


class LoginView(generic.edit.CreateView):
    form_class = forms.LoginForm
    template_name = 'events/user_login.html'
    action = '/login/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        
        form = self.form_class(initial=self.initial)

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        username = form.data.get('username')
        password = form.data.get('password')

        context = {'form': form}
        if username == '' or password == '':
            return render(request, self.template_name, context)

        user = authenticate(username=username, password=password)
        print(username+'--'+password)
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
    


class RegisterView(generic.edit.CreateView):
    model = User
    template_name = 'events/user_register.html'
    form_class = forms.UserSettingsForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})


class UserPasswordChangeView(generic.edit.UpdateView):
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
        """
        Modify the post method to to include errors
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.object = form.save()
            messages.success(request, 'Your password has been changed.')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(request, 'Your password was not changed.')
            return self.form_invalid(form)

class UserSettingsView(generic.edit.UpdateView):
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
        """
        Modify the post method to include errors
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.object = form.save()
            messages.success(request, 'Profile details updated.')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(request, 'Profile details remain unchanged. Fix the errors below first.')
            return self.form_invalid(form)


