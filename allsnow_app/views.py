# views.py
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .models import Tiendas, SolicitudLocal,Suscripcion, Registrarme
from .forms import SolicitudLocalForm, SolicitudUsuarioForm, RegistrarmeForm
from django.shortcuts import render
from .models import Tiendas
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def filtro_tiendas(request):
    # Filtra solo las tiendas con suscripción activa
    tiendas = Tiendas.objects.filter(estado_suscripcion='activa')  # Cambia 'activa' por el valor correspondiente si es diferente

    # Obtener los filtros
    region = request.GET.get('region')
    nombre_tienda = request.GET.get('nombre')

    # Verificar si hay filtros aplicados
    if region and region != "Seleccionar región":
        tiendas = tiendas.filter(region=region)

    if nombre_tienda:
        tiendas = tiendas.filter(nombre_tienda__icontains=nombre_tienda)

    # Si no se aplicó ningún filtro, no mostrar resultados
    if not region and not nombre_tienda:
        tiendas = Tiendas.objects.none()  # No devolver tiendas si no hay filtros

    # Obtener opciones de regiones
    regiones = Tiendas._meta.get_field('region').choices

    context = {
        'tiendas': tiendas,
        'selected_region': region,
        'regiones': regiones  # Agregar las opciones de región al contexto
    }
    return render(request, 'filtro_tienda.html', context)


def administrador(request):
    solicitudes = SolicitudLocal.objects.all()  # Obtener todas las solicitudes de tienda
    tiendas = Tiendas.objects.all()              # Obtener todas las tiendas
    suscripciones = Suscripcion.objects.all()    # Obtener todas las suscripciones

    context = {
        'solicitudes': solicitudes,
        'tiendas': tiendas,
        'suscripciones': suscripciones
    }
    
    return render(request, 'administrador.html', context)

def aprobar_solicitud(request, solicitud_id):
    # Obtiene la solicitud de tienda usando el campo correcto 'id_solicitud_tienda'
    solicitud = get_object_or_404(SolicitudLocal, id_solicitud_tienda=solicitud_id)
    
    # Crea una nueva entrada en Tiendas usando los datos de la solicitud
    Tiendas.objects.create(
        nombre=solicitud.nombre_tienda,
        # Asigna otros campos necesarios de la solicitud, como se definen en tu modelo Tiendas
        # por ejemplo: patente_local=solicitud.patente_local, region=solicitud.region
    )
    
    # Elimina la solicitud de tienda después de aprobarla
    solicitud.delete()
    return redirect(reverse('administrador'))

def rechazar_solicitud(request, solicitud_id):
    # Obtiene la solicitud de tienda usando el campo correcto 'id_solicitud_tienda'
    solicitud = get_object_or_404(SolicitudLocal, id_solicitud_tienda=solicitud_id)
    
    # Elimina la solicitud de tienda al rechazarla
    solicitud.delete()
    return redirect(reverse('administrador'))

def tienda_detalle(request, id):
    # Use the id to retrieve the store details
    tienda = Tiendas.objects.get(id_tienda=id)
    return render(request, 'tienda_detalle.html', {'tienda': tienda})

def inicio(request):
    return render(request, 'inicio.html')

def trabaja_con_nosotros(request):
    return render(request, 'inicio.html')

def registrarme(request):
    return render(request, 'inicio.html')

####### NATY <3 #############
def inventario_ventas(request):
    productos = Inventario.objects.all()  
    return render(request, 'inventario_ventas.html', {'productos': productos})

def inventario_arriendo(request):
    productos = InventarioArriendo.objects.all()  # Fetching all rental products
    return render(request, 'inventario_arriendo.html', {'productos': productos})

def tienda_detalle(request, id):
    # Use the id to retrieve the store details
    tienda = Tiendas.objects.get(id_tienda=id)
    return render(request, 'tienda_detalle.html', {'tienda': tienda})

#para agregar productos a la tabla ventas 
from django.shortcuts import render, redirect
from .models import Inventario, Tiendas 
from django.utils.formats import localize

def agregar_productos(request):
    if request.method == 'POST':
        # Obtén los datos del formulario
        id_tienda = request.POST.get('id_tienda')  
        nombre_producto = request.POST.get('nombre_producto')
        precio = request.POST.get('precio')
        cantidad_disponible = request.POST.get('cantidad_disponible')
        talla_producto = request.POST.get('talla_producto')

        # Crea una nueva instancia del modelo Inventario
        nuevo_producto = Inventario(
            id_tienda_id=id_tienda,  
            nombre_producto=nombre_producto,
            precio=precio,
            cantidad_disponible=cantidad_disponible,
            talla_producto=talla_producto
        )

        nuevo_producto.save()  
        # Formatear el precio
        formatted_price = localize(Inventario.precio)
        print(f'Precio formateado: ${formatted_price} CLP')

        return redirect('inventario_ventas')  

    return render(request, 'inventario_ventas.html')  

#para agregar datos a la tabla inventario arriendo
from django.shortcuts import render, redirect
from .models import InventarioArriendo

def agregar_productos_arriendo(request):
    if request.method == 'POST':
        id_tienda = request.POST.get('id_tienda')  
        nombre_producto = request.POST.get('nombre_producto')
        precio_arriendo = request.POST.get('precio_arriendo')
        cantidad_disponible = request.POST.get('cantidad_disponible')
        talla_producto = request.POST.get('talla_producto')

        # Crea una nueva instancia del modelo InventarioArriendo
        nuevo_producto_arriendo = InventarioArriendo(
            id_tienda_id=id_tienda,
            nombre_producto=nombre_producto,
            precio_arriendo=precio_arriendo,
            cantidad_disponible=cantidad_disponible,
            talla_producto=talla_producto
        )

        nuevo_producto_arriendo.save()  
        return redirect('inventario_arriendo')  

    return render(request, 'inventario_arriendo.html') 



# Vista para mostrar el inventario de arriendo
from django.shortcuts import render, redirect
from .models import InventarioArriendo
from .forms import InventarioArriendoForm 

def inventario_arriendo(request):
    if request.method == 'POST':
        if 'agregar' in request.POST:
            form = InventarioArriendoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('inventario_arriendo') 
            else:
                print(form.errors) 

    productos = InventarioArriendo.objects.all()
    return render(request, 'inventario_arriendo.html', {'productos': productos})

#para editar un producto de la tabla de inventario ventas
from django.shortcuts import render, redirect, get_object_or_404
from .models import Inventario

def editar_producto(request):
    if request.method == 'POST':
        id_producto = request.POST.get('id_producto')
        nombre_producto = request.POST.get('nombre_producto')
        cantidad_disponible = request.POST.get('cantidad_disponible')
        talla_producto = request.POST.get('talla_producto')
        precio = request.POST.get('precio')

        producto = get_object_or_404(Inventario, id_producto=id_producto)
        producto.nombre_producto = nombre_producto
        producto.cantidad_disponible = cantidad_disponible
        producto.talla_producto = talla_producto
        producto.precio = precio
        producto.save()

        return redirect('inventario_ventas')
     
#editar un producto de la tabla de inventario arriendo
from django.shortcuts import render, redirect, get_object_or_404
from .models import InventarioArriendo

def editar_producto_arriendo(request):
    if request.method == 'POST':
        id_producto = request.POST.get('id_producto')  # Obtén el ID del producto del formulario
        
        # Busca el producto usando el ID obtenido del formulario
        producto = get_object_or_404(InventarioArriendo, id_producto=id_producto)
        
        # Actualiza los campos del producto
        producto.nombre_producto = request.POST.get('nombre_producto')
        producto.cantidad_disponible = request.POST.get('cantidad_disponible')
        producto.talla_producto = request.POST.get('talla_producto')
        producto.precio_arriendo = request.POST.get('precio_arriendo')
        producto.save()

        return redirect('inventario_arriendo')  # Redirige a la vista de inventario

    return render(request, 'editar_producto_arriendo.html')  # Devuelve el formulario para editar


#eliminar producto de la tabla de arriendo
from django.shortcuts import redirect, get_object_or_404
from .models import InventarioArriendo 

def eliminar_producto_arriendo(request, id_producto):
    if request.method == 'POST':
        producto = get_object_or_404(InventarioArriendo, id_producto=id_producto)  
        producto.delete()  
        return redirect('inventario_arriendo') 
    return redirect('inventario_arriendo')  

#eliminar productos de la tabla deventa
from django.shortcuts import redirect, get_object_or_404
from .models import Inventario  

def eliminar_productos(request, id_producto):
    # Verifica que la solicitud sea POST
    if request.method == 'POST':
        # Busca el producto en InventarioArriendo usando el id_producto
        producto = get_object_or_404(Inventario, id_producto=id_producto) 
        producto.delete()  # Elimina el producto
        return redirect('inventario_ventas')  
    return redirect('inventario_ventas')  

def interfaz_dueno(request):
     return render(request, 'interfaz_dueno.html')


#para que se muestre el nombre de la tienda segun el dueño
from django.shortcuts import render
from .models import Usuarios, UsuarioTienda, Tiendas

def centro_rental_view(request):
    usuario = Usuarios.objects.get(id_usuario=request.user.id)
    usuario_tienda = UsuarioTienda.objects.filter(id_usuario=usuario).first()
    if usuario_tienda:
        tienda = usuario_tienda.id_tienda
        nombre_centro = f'CENTRO DE RENTAL "{tienda.nombre_tienda.upper()}"'
        descripcion = tienda.descripcion  
        ubicacion = tienda.ubicacion
    else:
        nombre_centro = "CENTRO DE RENTAL NO DISPONIBLE"
        descripcion = "No tienes un centro de rental asignado."
        ubicacion = "No tienes un centro de rental asignado."

    print(f'Nombre Centro: {nombre_centro}')  
    print(f'Descripción: {descripcion}')       
    print(f'Ubicación:{ubicacion}')

    context = {
        'nombre_centro': nombre_centro,
        'descripcion': descripcion,
        'ubicacion':ubicacion,
    }
    return render(request, 'interfaz_dueno.html', context)

#Para editar la descripcion de las tiendas por los dueños
def editar_descripcion_view(request):
     return render(request, 'editar_descripcion_view.html')

#para mostrar el interfaz de compra los productos de cada tienda 
from django.shortcuts import render, get_object_or_404
from .models import Inventario, Tiendas
from django.contrib.auth.decorators import login_required

@login_required
def interfaz_compra(request, id_tienda):
    tienda = get_object_or_404(Tiendas, id_tienda=id_tienda)
    productos = Inventario.objects.filter(id_tienda=tienda).order_by('nombre_producto')

    context = {
        'nombre_centro': tienda.nombre_tienda,
        'productos': productos,
    }

    return render(request, 'interfaz_compra.html', context)

#para comprar productos y agrgearlos al carro 

from django.shortcuts import render, get_object_or_404
from .models import Inventario
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def carro_de_compras(request, producto_id):
    usuario_id = request.user.id  # Obtiene el ID del usuario autenticado
    producto = get_object_or_404(Inventario, id_producto=producto_id)
    id_tienda = producto.id_tienda.id_tienda  # Obtén el ID de la tienda del producto

    if request.method == "POST":
        # Obtener el carrito específico del usuario desde la sesión
        carrito = request.session.get(f'carrito_{usuario_id}', {})

        # Agregar o actualizar la cantidad del producto en el carrito del usuario
        if producto_id in carrito:
            carrito[producto_id]['cantidad'] += 1
        else:
            carrito[producto_id] = {
                'nombre': producto.nombre_producto,
                'precio': float(producto.precio),
                'cantidad': 1
            }

        # Guardar el carrito de vuelta en la sesión
        request.session[f'carrito_{usuario_id}'] = carrito

        # Usar mensajes para mostrar un mensaje de éxito
        messages.success(request, f'Producto {producto.nombre_producto} agregado al carrito')

    # Renderiza la interfaz de compra y pasa el contexto
    return redirect('interfaz_compra', id_tienda=id_tienda)

###carro de arriendo 
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import InventarioArriendo

@login_required
def carro_de_arriendo(request, producto_id):
    usuario_id = request.user.id
    producto = get_object_or_404(InventarioArriendo, id_producto=producto_id)
    id_tienda = producto.id_tienda.id_tienda

    if request.method == "POST":
        carrito_arriendo = request.session.get(f'carrito_arriendo_{usuario_id}', {})

        if producto_id in carrito_arriendo:
            carrito_arriendo[producto_id]['cantidad'] += 1
        else:
            carrito_arriendo[producto_id] = {
                'nombre': producto.nombre_producto,
                'precio': float(producto.precio_arriendo),
                'cantidad': 1
            }

        request.session[f'carrito_arriendo_{usuario_id}'] = carrito_arriendo

        messages.success(request, f'Producto {producto.nombre_producto} agregado al carrito de arriendo')

    return redirect('interfaz_arriendo', id_tienda=id_tienda)


#para ver el carro de compras
from django.shortcuts import render
from .models import CarritoDeCompras

def ver_carro_de_compras(request):
    usuario_id = request.user.id  # ID del usuario actual
    id_tienda = request.session.get('id_tienda', 2)  # ID de la tienda (puedes cambiar la lógica según tu flujo)

    carrito = request.session.get(f'carrito_{usuario_id}', {})
    productos_carrito = []
    total_precio = 0.0

    for producto_id, detalles in carrito.items():
        # Crear o actualizar cada producto en la tabla CarritoDeCompras
        item_carrito, created = CarritoDeCompras.objects.update_or_create(
            usuario_id=usuario_id,
            tienda_id=id_tienda,
            producto_id=producto_id,
            defaults={
                'nombre_producto': detalles['nombre'],
                'precio': detalles['precio'],
                'cantidad': detalles['cantidad'],
                'subtotal': detalles['precio'] * detalles['cantidad']
            }
        )
        productos_carrito.append({
            'id_producto': producto_id,
            'nombre': detalles['nombre'],
            'precio': detalles['precio'],
            'cantidad': detalles['cantidad'],
            'subtotal': detalles['precio'] * detalles['cantidad'],
        })
        total_precio += detalles['precio'] * detalles['cantidad']
    context = {
        'productos_carrito': productos_carrito,
        'total_precio': total_precio,
        'id_tienda': id_tienda,
    }
    return render(request, 'ver_carro_de_compras.html', context)

#para ver el carro_de_arriendo
from django.shortcuts import render
from .models import CarritoDeArriendo

def ver_carro_de_arriendo(request):
    usuario_id = request.user.id  
    id_tienda = request.session.get('id_tienda',1)  
    carrito_arriendo = request.session.get(f'carrito_arriendo_{usuario_id}', {})
    productos_carrito = []
    total_precio = 0.0

    for producto_id, detalles in carrito_arriendo.items():
        # Crear o actualizar cada producto en la tabla CarritoDeArriendo
        item_carrito, created = CarritoDeArriendo.objects.update_or_create(
            usuario_id=usuario_id,
            tienda_id=id_tienda,
            producto_id=producto_id,
            defaults={
                'nombre_producto': detalles['nombre'],
                'precio': detalles['precio'],
                'cantidad': detalles['cantidad'],
                'subtotal': detalles['precio'] * detalles['cantidad']
            }
        )
        productos_carrito.append({
            'id_producto': producto_id,
            'nombre': detalles['nombre'],
            'precio': detalles['precio'],
            'cantidad': detalles['cantidad'],
            'subtotal': detalles['precio'] * detalles['cantidad'],
        })
        total_precio += detalles['precio'] * detalles['cantidad']
    context = {
        'productos_carrito': productos_carrito,
        'total_precio': total_precio,
        'id_tienda': id_tienda,
    }
    return render(request, 'ver_carro_de_arriendo.html', context)


#para eliminar productos del carro de compra

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def eliminar_producto(request, producto_id):
    usuario_id = request.user.id
    carrito_key = f'carrito_{usuario_id}'
    carrito = request.session.get(carrito_key, {})

    # Eliminar el producto del carrito si existe
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session[carrito_key] = carrito  

    return redirect('ver_carro_de_compras')  

# eliminar productos del carro de arriendo

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def eliminar_producto_arriendo(request, producto_id):
    usuario_id = request.user.id
    carrito_key = f'carrito_arriendo_{usuario_id}'
    carrito_arriendo = request.session.get(carrito_key, {})

    # Eliminar el producto del carrito si existe
    if str(producto_id) in carrito_arriendo:
        del carrito_arriendo[str(producto_id)]
        request.session[carrito_key] = carrito_arriendo  

    return redirect('ver_carro_de_arriendo')  


#actualizar la cantidad de productos en el carro de compras
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CarritoDeCompras

@login_required
def actualizar_cantidad(request, producto_id):
    if request.method == 'POST':
        nueva_cantidad = int(request.POST.get('cantidad'))
        usuario_id = request.user.id
        carrito_key = f'carrito_{usuario_id}'
        carrito = request.session.get(carrito_key, {})

        # Actualiza la cantidad en la sesión y en la base de datos
        if str(producto_id) in carrito:
            if nueva_cantidad > 0:
                # Actualiza la cantidad y subtotal
                carrito[str(producto_id)]['cantidad'] = nueva_cantidad
                carrito[str(producto_id)]['subtotal'] = carrito[str(producto_id)]['precio'] * nueva_cantidad
                request.session[carrito_key] = carrito
                # Actualizar en la base de datos
                CarritoDeCompras.objects.filter(usuario_id=usuario_id, producto_id=producto_id).update(
                    cantidad=nueva_cantidad,
                    subtotal=carrito[str(producto_id)]['subtotal']
                )
            else:
                # Elimina el producto si la cantidad es 0
                del carrito[str(producto_id)]
                request.session[carrito_key] = carrito
                CarritoDeCompras.objects.filter(usuario_id=usuario_id, producto_id=producto_id).delete()

    return redirect('ver_carro_de_compras')


#para mostrar el interfaz de arriendo los productos de cada tienda 
from django.shortcuts import render, get_object_or_404
from .models import InventarioArriendo, Tiendas  
from django.contrib.auth.decorators import login_required

@login_required
def interfaz_arriendo(request, id_tienda):
    tienda = get_object_or_404(Tiendas, id_tienda=id_tienda)
    productos = InventarioArriendo.objects.filter(id_tienda=tienda).order_by('nombre_producto')  
    context = {
        'nombre_centro': tienda.nombre_tienda,  
        'productos': productos,
    }

    return render(request, 'interfaz_arriendo.html', context)


####PAULA MIKAL INICIO####



def inicio(request):
    return render(request, 'inicio.html')


def trabaja_con_nosotros(request):
    return render(request, 'trabaja_con_nosotros.html')


def registrarme(request):
    form = RegistrarmeForm()
    if request.method == 'POST':
        form = RegistrarmeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrarme_exitoso')  # Asegúrate de tener esta URL configurada
    return render(request, 'registrarme.html', {'form_registrarme': form})


def registrar_local(request):
    return render(request, 'registrar_local.html')

def registrarme_exitoso(request):
    return render(request, 'registrarme_exitoso.html')



def trabaja_con_nosotros(request):
    if request.method == 'POST':
        form_usuario = SolicitudUsuarioForm(request.POST)
        form_local = SolicitudLocalForm(request.POST)

        if form_usuario.is_valid() and form_local.is_valid():
            # Crear una instancia de usuario sin guardarla aún en la base de datos
            usuario = form_usuario.save(commit=False)
            usuario.save()  # Guarda el usuario en la base de datos

            # Crear una instancia de local asociada al usuario sin guardarla aún
            local = form_local.save(commit=False)
            local.usuario = usuario  # Asocia el local al usuario
            local.save()  # Guarda el local en la base de datos

            # Redirecciona o realiza alguna acción después de guardar
            return redirect('registrar_local')
    else:
        form_usuario = SolicitudUsuarioForm()
        form_local = SolicitudLocalForm()

    return render(request, 'trabaja_con_nosotros.html', {
        'form_usuario': form_usuario,
        'form_local': form_local,
    })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                # Buscamos al usuario en la tabla 'Registrarme'
                user = Registrarme.objects.get(correo=email)

                # Compara la contraseña directamente sin hash
                if password == user.contraseña:  # Compara en texto plano
                    # Iniciar sesión creando una variable de sesión manualmente
                    request.session['user_id'] = user.id
                    return redirect('filtro_tienda')  # Redirige a la vista 'filtro_tienda'

                else:
                    messages.error(request, "Correo o contraseña incorrecta")

            except Registrarme.DoesNotExist:
                # Si el usuario no existe, muestra un mensaje de error
                messages.error(request, "Correo o contraseña incorrecta")
    
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

####PAULA MIKAL FIN####
