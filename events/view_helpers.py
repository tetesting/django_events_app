from django.http import HttpResponseRedirect

from django.contrib import messages


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

