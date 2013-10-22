from django import forms
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone

from events import models


ONE_HOUR = timezone.timedelta(0,3600)

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
      attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
      attrs={'placeholder':'Password'}))


    def __init__(self, *args, **kwargs):
        return super(LoginForm, self).__init__(*args, **kwargs)


class RegisterForm(forms.ModelForm):
    username = forms.CharField(required=True)
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True)

    class Meta:
        model = models.User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 
            'location', 'description')

    def __init__(self, *args, **kwargs):
        return super(RegisterForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        password = cleaned_data.get('password')
        password_confirm =cleaned_data.get('password_confirm')

        # check if passwords match
        if password_confirm:
            if password != password_confirm:
                errors = ['The passwords must match.']
                self.errors['password_confirm'] = self.error_class(errors)
                raise forms.ValidationError(errors[0])
            else:
                cleaned_data['password'] = make_password(password)

        return cleaned_data

class UserSettingsForm(forms.ModelForm):

    # tags = forms.CharField(widget=forms.TextInput(attrs={'value':'cool'}))

    class Meta:
        model = models.User
        fields = ('username', 'first_name', 'last_name', 'email', 
            'location', 'description')


class UserPasswordChangeForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True)

    password_new = forms.CharField(
        widget=forms.PasswordInput(),
        required=True)
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        required=True)
    

    def clean(self):
        cleaned_data = super(UserPasswordChangeForm, self).clean()

        password = cleaned_data.get('password')
        encoded = self.instance.password

        if not check_password(password, encoded):
            error_message = 'Incorrect password.'
            self.errors['password'] = self.error_class([error_message])
            raise forms.ValidationError(error_message)

        password_new = cleaned_data.get('password_new')
        password_confirm = cleaned_data.get('password_confirm')

        if password_new and password_confirm:
            if password_confirm != password_new:
                error_message = 'The new passwords must match.'
                self.errors['password_confirm'] = self.error_class([error_message])
                raise forms.ValidationError(error_message)

        cleaned_data['password'] = make_password(password_confirm)

        return cleaned_data


class CreateEventForm(forms.ModelForm):

    class Meta:
        model = models.Event
        exclude = ['organizer_id']

    def __init__(self, *args, **kwargs):
        kwargs['initial'].update({'start_date': timezone.now()+ONE_HOUR})
        return super(CreateEventForm, self).__init__(*args, **kwargs)


class EventForm(forms.ModelForm):

    class Meta:
        model = models.Event
        fields = ['name', 'start_date', 'end_date', 'location', 'description']




