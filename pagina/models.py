from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

# Create your models here.
class Categoria(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

class Item(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="clasificacion")
    titulo = models.CharField(max_length=100, null=False)
    precio = models.IntegerField(default=0)
    contenido = models.CharField(max_length=1000, null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_edicion = models.DateTimeField(auto_now=True)
    imagen = models.ImageField(upload_to='images/', null=True)
    editor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="publicador")

    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse("detail", kwargs={
            "item_id": self.Item_id
        })
    
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuario")
    compras = models.ManyToManyField(Item)

    def __str__(self):
        return f"{self.usuario} - {self.compras}"

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    consulta = models.TextField()
    avisos = models.BooleanField('deseo recibir avisos')

    def __str__(self):
        return self.correo
    