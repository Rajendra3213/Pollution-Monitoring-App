from django import forms
from .models import TreePlantation
from django.forms import ModelForm

class LoginForm(forms.Form):
   email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
   password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class DonationForm(ModelForm):
    PLANTED_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]

    planted = forms.ChoiceField(
        choices=PLANTED_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = TreePlantation
        fields = ('longitude', 'latitude', 'planted')
        widgets = {
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
        }