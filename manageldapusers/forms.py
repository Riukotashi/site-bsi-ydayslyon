
from django import forms
from .models import LdapUser

class registerForm(forms.Form):

    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control'}))
    # className = forms.CharField(label="classe", widget=forms.ChoiceField(choices = CHOICES))
    className= forms.CharField(label='Classe', widget=forms.Select(choices = LdapUser.CHOICES))