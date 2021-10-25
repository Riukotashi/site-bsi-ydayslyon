
from django import forms

from .models import LdapUser

class LdapUserForm(forms.ModelForm):

    class Meta:
        model = LdapUser
        fields = ("name", "surname", "email", "password")
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Nom',
                    'class': 'w-full px-3 py-2 outline-none text-black',
                }
            ),
            'surname': forms.TextInput(
                attrs={
                    'placeholder': 'Prénom',
                    'class': 'w-full px-3 py-2 outline-none text-black',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Adresse Email',
                    'class': 'w-full px-3 py-2 outline-none text-black',
                }
            ),
            'password': forms.TextInput(
                attrs={
                    'placeholder': 'Nom',
                    'class': 'w-full px-3 py-2 outline-none text-black',
                }
            ),
        }