from django import forms
from django.contrib.auth.hashers import check_password, make_password

from events import models


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
      attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
      attrs={'placeholder':'Password'}))


    def __init__(self, *args, **kwargs):
        return super(LoginForm, self).__init__(*args, **kwargs)


class RegisterForm(forms.ModelForm):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = models.User

    def __init__(self, *args, **kwargs):
        return super(RegisterForm, self).__init__(*args, **kwargs)


class UserSettingsForm(forms.ModelForm):
    # username = forms.CharField(required=True)

    tags = forms.CharField(widget=forms.TextInput(
      attrs={'value':'cool'}))

    class Meta:
        model = models.User
        fields = ('username', 'first_name', 'last_name', 'email', 
            'location', 'description')


class UserPasswordChangeForm(forms.ModelForm):
 
    password_new = forms.CharField(
        widget=forms.PasswordInput(),
        required=True)
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True)


    def __init__(self, *args, **kwargs):
        return super(UserPasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_password_confirm(self):
        password_new = self.cleaned_data.get('password_new')
        password_confirm = self.cleaned_data.get('password_confirm')
        
        if password_new:
            errors = []
            if password_confirm != password_new:
                errors.append('The passwords did not match.')
            if errors:
                self.errors['password_confirm'] = self.error_class(errors)

        return password_confirm

    def clean_password(self):
        password = self.cleaned_data.get('password')
        encoded = self.instance.password
        
        if 'password_confirm' not in self.errors:
            if not check_password(password, encoded):
                self.errors['password'] = \
                    self.error_class(['Incorrect password.'])
        
        return make_password(self.cleaned_data.get('password_confirm'))

