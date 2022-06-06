import requests
from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import *
from .models import *
from app.models import Producto

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required

#El view se comporta como un controlador.
#Conecta con el modelo.

#QRUD Seccion > Listar
def home(request):
    productosAll = Producto.objects.all()
    
    #JSON > Recoge la variable productosAll, que a su vez contiene todas las variables del modelo (DB)
    datos = {
        'listaProductos' : productosAll
    }

    return render(request, 'app/home.html', datos)

@permission_required('app.add_producto')
#CRUD Seccion > Agregar (CREATE)
def agregar_producto(request):
    datos = {
        'form': ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            datos['mensaje'] = "Producto agregado correctamente!"
        else:
            datos['form'] = formulario

    return render(request, 'app/productos/agregar_producto.html', datos)


@permission_required('app.change_producto')
#CRUD Seccion > Modificar (UPDATE)
def modificarProducto(request, cod):
    producto = Producto.objects.get(cod=cod)
    datos = {
        'form' : ProductoForm(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES, instance=producto)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "¡Producto modificado correctamente!")
            return redirect(to=listarProductos)
        datos['form'] = formulario
    
    return render(request, 'app/productos/modificarProducto.html', datos)

@permission_required('app.view_producto')
#CRUD Seccion > Leer (READ)
def listarProductos(request):
    productosAll = Producto.objects.all()
    
    #JSON > Recoge la variable productosAll, que a su vez contiene todas las variables del modelo (DB)
    datos = {
        'listaProductos' : productosAll
    }

    return render(request, 'app/productos/listarProductos.html', datos)

@permission_required('app.delete_producto')
#CRUD Seccion > Delete ()
def eliminarProducto(request, cod):
    producto = Producto.objects.get(cod=cod)
    producto.delete()
    messages.success(request, "¡Producto eliminado correctamente!")

    return redirect(to="listarProductos")

def aboutUs(request):
    return render(request, 'app/about-us.html')

@login_required
def cart(request):
    carro = ItemsCarro.objects.all()  
    #JSON > Recoge la variable productosAll, que a su vez contiene todas las variables del modelo (DB)
    datos = {
        'listaCarro' : carro
    }

    return render(request, 'app/cart.html', datos)

@login_required
def donation(request):
    return render(request, 'app/donation.html')

@login_required
def success(request):
    carro = ItemsCarro.objects.all()
    carro.delete()

    return render(request, 'app/success.html')

@login_required
def historial(request):
    carro = ItemsCarro.objects.all()
    
    #JSON > Recoge la variable productosAll, que a su vez contiene todas las variables del modelo (DB)
    datos = {
        'listaCarro' : carro
    }

    return render(request, 'app/historial.html', datos)

@login_required
def indexLog(request):
    productosAll = Producto.objects.all()
    
    #JSON > Recoge la variable productosAll, que a su vez contiene todas las variables del modelo (DB)
    datos = {
        'listaProductos' : productosAll
    }

    if request.method == 'POST':
        carro = ItemsCarro()
        #Rellenamos el carro con los datos que vienen de POST
        carro.imagen = request.POST.get('imagen')
        carro.nombre_producto = request.POST.get('nombre_producto')
        carro.precio_producto = request.POST.get('precio_producto')
        carro.save()

    return render(request, 'app/index-log.html', datos)

def login(request):
    datos = {
        'form': SesionForm()
    }

    return render(request, 'app/login.html', datos)

@login_required
def products(request):
    productosAll = Producto.objects.all()
    response = requests.get('http://127.0.0.1:8000/api/productos/').json()
    
    #JSON > Recoge la variable productosAll, que a su vez contiene todas las variables del modelo (DB)
    datos = {
        'listaProductos' : productosAll,
        'listaJson' : response,
    }
    
    if request.method == 'POST':
        carro = ItemsCarro()
        #Rellenamos el carro con los datos que vienen de POST
        carro.imagen = request.POST.get('imagen')
        carro.nombre_producto = request.POST.get('nombre_producto')
        carro.precio_producto = request.POST.get('precio_producto')
        carro.save()

    return render(request, 'app/products.html', datos)

def register(request):
    datos = {
        'form': RegistroForm()
    }

    return render(request, 'app/register.html', datos)

def registro(request):
    datos = {
        'form' : RegistroUserForm()
    }

    if request.method == 'POST':
        formulario = RegistroUserForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="login")
        datos["form"] = formulario

    return render(request, 'registration/registro.html', datos)

@login_required
def suscribe(request):
    usuarioAll = Usuario.objects.all()
    
    #JSON > Recoge la variable productosAll, que a su vez contiene todas las variables del modelo (DB)
    datos = {
        'listaUsuarios' : usuarioAll
    }

    return render(request, 'app/suscribe.html', datos)

@permission_required('app.add_usuario')
#CRUD Seccion > Agregar (CREATE)
def agregarUsuario(request):
    datos = {
        'form': UsuarioForm()
    }
    if request.method == 'POST':
        formulario = UsuarioForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            datos['mensaje'] = "Usuario agregado correctamente!"
        else:
            datos['form'] = formulario

    return render(request, 'app/usuarios/agregarUsuario.html', datos)

@permission_required('app.change_usuario')
#CRUD Seccion > Modificar (UPDATE)
def modificarUsuario(request, cod_usuario):
    usuario = Usuario.objects.get(cod_usuario=cod_usuario)
    datos = {
        'form' : UsuarioForm(instance=usuario)
    }
    if request.method == 'POST':
        formulario = UsuarioForm(data=request.POST, files=request.FILES, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "¡Usuario modificado correctamente!")
            return redirect(to=listarUsuario)
        datos['form'] = formulario
    
    return render(request, 'app/usuarios/modificarUsuario.html', datos)

@permission_required('app.view_usuario')
#CRUD Seccion > Leer (READ)
def listarUsuario(request):
    usuarioAll = Usuario.objects.all()
    
    #JSON > Recoge la variable productosAll, que a su vez contiene todas las variables del modelo (DB)
    datos = {
        'listaUsuarios' : usuarioAll
    }

    return render(request, 'app/usuarios/listarUsuario.html', datos)

@permission_required('app.delete_usuario')
#CRUD Seccion > Delete ()
def eliminarUsuario(request, cod_usuario):
    usuario = Usuario.objects.get(cod_usuario=cod_usuario)
    usuario.delete()
    messages.success(request, "¡Usuario eliminado correctamente!")

    return redirect(to="listarUsuario")

@login_required
def despacho(request):
    return render(request, 'app/despacho.html')



