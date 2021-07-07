
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import NuevoItem, CustomUserCreationForm, ContactoForm
from .models import Item, Categoria, Carrito
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q


# Create your views here.
def index(request):
    busq = request.GET.get("buscar")
    items = Item.objects.all()
    if busq:
        items = items.filter(
            Q(titulo__icontains = busq) |
            Q(contenido__icontains = busq)
        ).distinct()
    lista_categorias = reversed(Categoria.objects.all())
    if "carrito" not in request.session:
        request.session["carrito"] = []
    return render(request, 'pagina/index.html', {
        "lista_items": items,
        "lista_categorias": lista_categorias,
        "lista_carrito": request.session["carrito"],
    })

def itemView(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'pagina/item_vista.html', {
        "item": item,
        "lista_categorias": Categoria.objects.all(),
        "lista_carrito": request.session["carrito"],
    })

@permission_required('pagina.add_item')
def itemCreate(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        form = NuevoItem(request.POST, request.FILES, instance=Item(imagen=request.FILES['imagen'], editor=user))
        if form.is_valid():
            form.save()
            return redirect('pagina:index', {
                "lista_categorias": Categoria.objects.all(),
            })
    else:
        form = NuevoItem(initial={'fecha_creacion':timezone.now()})
        return render(request, 'pagina/item_crear.html', {
            "form": form,
            "lista_categorias": Categoria.objects.all(),
        })

@permission_required('pagina.change_item')
def itemUpdate(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == "POST":  
        user = User.objects.get(username=request.user)   
        item.editor = user
        form = NuevoItem(data=request.POST, files=request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect("pagina:index")
    else:
        form = NuevoItem(instance = item)
        return render(request, 'pagina/item_edicion.html', {
            "item": item,
            "form": form
        })

@permission_required('pagina.delete_item')
def itemDelete(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect("pagina:index")


def filtroCategoria(request, categoria_id):
    filtro = get_object_or_404(Categoria, id=categoria_id)
    items = Item.objects.all()
    items = items.filter(categoria=filtro)
    return render(request, 'pagina/index.html', {
        "lista_items": items,
        "lista_categorias": Categoria.objects.all(),
        "categoria_filtro": filtro
    })

@login_required
def carrito(request, item_id):
    un_item = get_object_or_404(Item, id=item_id)
    for i in request.session["carrito"]:
        if i["id"] == un_item.id:
            #existe el item
            return HttpResponseRedirect(reverse("pagina:vista", args=(un_item.id,)))            
    #request.session["carrito"] += [(un_item.titulo, un_item.precio)]
    request.session["carrito"] += [{
        "titulo": un_item.titulo,
        "precio": un_item.precio,
        "id": un_item.id
    }]
    return HttpResponseRedirect(reverse("pagina:vista", args=(un_item.id,)))

@login_required
def carritoEliminar(request, item_id):
    un_item = get_object_or_404(Item, id=item_id) #objeto entero

    for i in request.session["carrito"]:
        if i == un_item:
            carritod = request.session["carrito"]
            carritod.remove(i)
            request.session["carrito"] = carritod
        return render(request, 'pagina/carrito.html')
    
@login_required
def botonCarrito(request):
    carrito = request.session["carrito"]
    return render(request, 'pagina/carrito.html', {
        "lista_carrito": carrito,
        "lista_categorias": Categoria.objects.all(),
    })


def acercade(request):
    return render(request, 'pagina/acerca_de.html', {
        "lista_categorias": Categoria.objects.all(),
    })

def contacto(request):
    form = ContactoForm()

    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save

    return render(request, 'pagina/contacto.html', {
        "lista_categorias": Categoria.objects.all(),
        "form": form
    })

def registro(request):
    data = {
        "form": CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            return redirect('pagina:index')
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)
