from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreationFormCostum(UserCreationForm):
    email = forms.EmailField(required=True , label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("about", "picture")
        widgets = {
            'about':forms.Textarea(attrs={'rows':10, 'cols':70})
            }