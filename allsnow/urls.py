"""allsnow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from allsnow_app import views
from allsnow_app.views import agregar_productos_arriendo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('filtro_tienda/', views.filtro_tiendas, name='filtro_tienda'),
    path('administrador/', views.administrador, name='administrador'),
    path('', views.inicio, name='inicio'),
    path('trabaja-con-nosotros/', views.trabaja_con_nosotros, name='trabaja_con_nosotros'),
    path('registrarme/', views.registrarme, name='registrarme'),
    path('registrar_local/', views.registrar_local, name='registrar_local'),
    path('registrarme_exitoso/', views.registrarme_exitoso, name='registrarme_exitoso'),
    path('login/', views.login_view, name='login'),
    path('aprovar-solicitud/<int:solicitud_id>/', views.aprobar_solicitud, name='aprobar_solicitud'),
    path('rechazar-solicitud/<int:solicitud_id>/', views.rechazar_solicitud, name='rechazar_solicitud'),
    path('tienda/<int:id>/', views.tienda_detalle, name='tienda_detalle'),
    path('inventario_ventas/', views.inventario_ventas, name='inventario_ventas'),
    path('agregar_productos/', views.agregar_productos, name='agregar_productos'),
    path('editar_producto_arriendo/<int:id_producto>/', views.editar_producto_arriendo, name='editar_producto_arriendo'),
    path('inventario_arriendo/', views.inventario_arriendo, name='inventario_arriendo'),
    path('agregar_producto_arriendo/', agregar_productos_arriendo, name='agregar_productos_arriendo'),
    path('eliminar_producto_arriendo/<int:id_producto>/', views.eliminar_producto_arriendo, name='eliminar_producto_arriendo'),
    path('eliminar_productos/<int:id_producto>/', views.eliminar_productos, name='eliminar_productos'),
    path('editar_producto/', views.editar_producto, name='editar_producto'),
    path('interfaz_dueno/', views.interfaz_dueno, name='interfaz_dueno'),
    path('centro_rental_view/', views.centro_rental_view, name='centro_rental_view'),
    path('editar_descripcion_view/', views.editar_descripcion_view, name='editar_descripcion_view'),
    path('interfaz_compra/<int:id_tienda>/', views.interfaz_compra, name='interfaz_compra'),
    path('carro_de_compras/<int:producto_id>/', views.carro_de_compras, name='carro_de_compras'),
    path('ver_carro_de_compras/', views.ver_carro_de_compras, name='ver_carro_de_compras'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('eliminar_producto_arriendo/<int:producto_id>/', views.eliminar_producto_arriendo, name='eliminar_producto_arriendo'),
    path('actualizar_cantidad/<int:producto_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('interfaz_arriendo/<int:id_tienda>/', views.interfaz_arriendo, name='interfaz_arriendo'),
    path('carro_de_arriendo/<int:producto_id>/', views.carro_de_arriendo, name='carro_de_arriendo'),
    path('carro_de_arriendo/', views.ver_carro_de_arriendo, name='ver_carro_de_arriendo'),
]
