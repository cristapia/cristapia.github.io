from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from datetime import datetime
from django import forms
from .models import *
from django.forms import inlineformset_factory

class CreateUserForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = ['username','email','password1','password2']

        def clean_email(self):
            email = self.cleaned_data["email"]
            revisaEmail = Usuario.objects.filter(email__iexact = email).exists()

            if revisaEmail:
                raise ValidationError("El correo ingresado ya se encuentra registrado")
            else:
                return email

class CapituloForm(forms.ModelForm):
    class Meta:
        model = Capitulos
        fields = ['titulo_capitulo', 'contenido']

class CrearObra(forms.ModelForm):

    usuario = forms.ModelChoiceField(queryset=Usuario.objects.all(), widget=forms.HiddenInput())
    CrearCapitulo = inlineformset_factory(Obra, Capitulos, fields=['titulo_capitulo', 'contenido'], extra=1)

    class Meta:
        model = Obra
        fields = ['foto_obra', 'titulo', 'sinopsis', 'restriccion', 'usuario']

class FormularioUserResgistro(UserCreationForm):

    class Meta:
        model = Usuario
        fields = ['username','first_name','last_name','email','password1','password2']

    def clean_email(self):
        email = self.cleaned_data["email"]
        revisaEmail = Usuario.objects.filter(email__iexact = email).exists()

        if revisaEmail:
            raise ValidationError("El correo ingresado ya se encuentra registrado")
        else:
            return email

class FormularioComentario(forms.ModelForm):
    class Meta:
        model = Comentarios
        fields = ['contenido']

class EditarObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['titulo', 'sinopsis', 'restriccion']

class CapituloForm(forms.ModelForm):
    class Meta:
        model = Capitulos
        fields = ['titulo_capitulo', 'contenido']
        widgets = {
            'titulo_capitulo': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control'}),
        }
    
class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['fecha_nacimiento', 'first_name', 'foto_perfil', 'last_name', 'sobre_mi', 'facebook', 'twitter', 'instagram', 'tumblr']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False