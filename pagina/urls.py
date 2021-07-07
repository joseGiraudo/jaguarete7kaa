from django.urls import path
from . import views
from django.urls import reverse

app_name = "pagina"
urlpatterns = [
    path('', views.index, name="index"),
    path('item/<int:item_id>', views.itemView, name="vista"),
    path('carrito/<int:item_id>', views.carrito, name="carrito"),
    path('carritoEliminar/<int:item_id>', views.carritoEliminar, name="carritoEliminar"),
    path('item/crear', views.itemCreate, name="nuevo"),
    path('item/editar/<int:item_id>', views.itemUpdate, name="editar"),
    path('item/eliminar/<int:item_id>', views.itemDelete, name="eliminar"),
    path('categoria/<int:categoria_id>', views.filtroCategoria, name="categoria"),
    path('vistaCarrito', views.botonCarrito, name="vistaCarrito"),
    path('acercade', views.acercade, name="acercade"),
    path('contacto', views.contacto, name="contacto"),
    path('registro', views.registro, name="registro"),
]