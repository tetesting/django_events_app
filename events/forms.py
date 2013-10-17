from django import forms

from events import models


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
      attrs={'style': '', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
      attrs={'style': '','placeholder':'Password'}))


    def __init__(self, *args, **kwargs):
        return super(LoginForm, self).__init__(*args, **kwargs)


class RegisterForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = models.User

    def __init__(self, *args, **kwargs):
        return super(LoginForm, self).__init__(*args, **kwargs)