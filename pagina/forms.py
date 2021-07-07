from django import forms
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Item, Contacto

class NuevoItem(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = ['titulo', 'categoria', 'precio', 'contenido', 'imagen']

        widgets = {
            "fecha_creacion": forms.SelectDateWidget()
        }

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class ContactoForm(forms.ModelForm):

    class Meta:
        model = Contacto
        fields = '__all__'