from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mfa_secret = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.user.username

from django.db import models

class Sobremesa(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    imagem = models.ImageField(upload_to='sobremesas/')

    def __str__(self):
        return self.nome

