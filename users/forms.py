from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'phone')
        # add phone number field here when added to model

        labels = {'email': 'Email*', 'username': 'Username*'}

    password1 = forms.CharField(label="Password*", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password*", widget=forms.PasswordInput)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
