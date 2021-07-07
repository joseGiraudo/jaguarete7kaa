from django.contrib import admin
from .models import Item, Categoria, Carrito, Contacto

# Register your models here.
admin.site.register(Item)
admin.site.register(Categoria)
admin.site.register(Carrito)
admin.site.register(Contacto)