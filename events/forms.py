from django import forms

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
        return super(LoginForm, self).__init__(*args, **kwargs)


class UserForm(forms.ModelForm):
    # username = forms.CharField(required=True)

    tags = forms.CharField(widget=forms.TextInput(
      attrs={'value':'shit'}))

    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = models.User
        fields = ('username', 'first_name', 'last_name', 'email', 
            'location', 'description', 'tags')
