import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

class Usuario(AbstractUser):
    fecha_nacimiento = models.DateField(null=True, blank=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfiles/', null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='usuario_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='usuario_permissions')
    sobre_mi = models.TextField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    tumblr = models.URLField(blank=True, null=True)

    def get_all_likes(self):
        return Like.objects.filter(capitulo__obra__usuario=self)

class Obra(models.Model):
    titulo = models.CharField(max_length=100)
    sinopsis = models.TextField()
    restriccion = models.BooleanField(default=False)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    foto_obra = models.ImageField(upload_to='fotos_obras/', null=True, blank=True)
    search_vector = SearchVectorField(null=True, blank=True)
    class Meta:
        indexes = [GinIndex(fields=['search_vector'])]

    def get_total_likes(self):
        return Like.objects.filter(capitulo__obra=self).values('user').distinct().count()
    
    def get_total_likes_all_capitulos(self):
        return Like.objects.filter(capitulo__obra=self).count()

class Capitulos(models.Model):
    titulo_capitulo = models.CharField(max_length=100)
    contenido = models.TextField()
    orden = models.IntegerField(default=0)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='capitulos')

    def save(self, *args, **kwargs):
        self.orden = (Capitulos.objects.filter(obra=self.obra)
                                     .aggregate(models.Max('orden'))['orden__max'] or 0) + 1
        super(Capitulos, self).save(*args, **kwargs)

class Comentarios(models.Model):
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    capitulo = models.ForeignKey(Capitulos, on_delete=models.CASCADE)

class Like(models.Model):
    capitulo = models.ForeignKey(Capitulos, related_name='capitulo_likes', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.capitulo.obra.titulo}"


