from django import forms
from django.forms import widgets
from .models import Search, Comment




class ComentariosForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}),label='Nombre:')
    body = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","rows":3}),label='Comentario:')

    class Meta:
        model = Comment
        fields = ['nombre','body',] 

class Latitud_Longitud(forms.Form):
    post = forms.CharField(label='Latitud,Longitud:')

class SearchForm(forms.ModelForm):
    address = forms.CharField(label='Ingrese la dirección del incendio: ')

    class Meta:
        model = Search
        fields = ['address',]
