from django.http import HttpResponseRedirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import Event, User


class LoginRequiredMixin(object):

    @method_decorator(login_required(redirect_field_name=''))
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class SaveViewWithMessageMixin(object):

    def post(self, request, message_dict, *args, **kwargs):
        """
        Modify the post method to include messages
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.object = form.save()
            messages.success(request, message_dict['success'])
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(request, message_dict['error'])
            return self.form_invalid(form)


class MyEventsMixin(object):

    def get_events_organizing(self, limit=6):
        """"Return the soonest upcoming events that the user is organizing."""
        return Event.objects.filter(organizer=self.request.user,
            start_date__gte=timezone.now()).order_by('start_date')[:limit]

    def get_events_attending(self, limit=6):
        """"Return the soonest upcoming events that the user is attending."""
        return User.objects.get(pk=self.request.user.id).events_attendees_set.filter(start_date__gte=timezone.now()).order_by('start_date')[:limit]


class SingleEventMixin(object):

    def get_success_url(self):
        try:
            url = "/{}/".format(self.object.id)
        except AttributeError:
            raise ImproperlyConfigured(
                "No URL to redirect to.  Either provide a url or define"
                " a get_absolute_url method on the Model.")
        return url





