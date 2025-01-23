from django import forms
from .models import Sobremesa

class SobremesaForm(forms.ModelForm):
    class Meta:
        model = Sobremesa
        fields = ['nome', 'descricao', 'preco', 'imagem']  # Ajuste os campos conforme o modelo Sobremesa
