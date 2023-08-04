from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    phone_number = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'birth_date', 'phone_number')