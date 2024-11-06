from django.db import models
from django.contrib.auth.hashers import make_password
# Create your models here.

class RolUsuario(models.Model):
    id_rol = models.AutoField(primary_key=True)
    rol = models.CharField(max_length=50)

    class Meta:
        db_table = 'Rol_Usuario'


class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    contraseña = models.CharField(max_length=225)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Usuarios'


class Tiendas(models.Model):
    id_tienda = models.AutoField(primary_key=True)
    nombre_tienda = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=225)
    region = models.CharField(
        max_length=100,
        choices=[
            ("Arica y Parinacota", "Arica y Parinacota"),
            ("Tarapacá", "Tarapacá"),
            ("Antofagasta", "Antofagasta"),
            ("Atacama", "Atacama"),
            ("Coquimbo", "Coquimbo"),
            ("Valparaíso", "Valparaíso"),
            ("Metropolitana de Santiago", "Metropolitana de Santiago"),
            ("Libertador General Bernardo O'Higgins", "Libertador General Bernardo O'Higgins"),
            ("Maule", "Maule"),
            ("Ñuble", "Ñuble"),
            ("Biobío", "Biobío"),
            ("La Araucanía", "La Araucanía"),
            ("Los Ríos", "Los Ríos"),
            ("Los Lagos", "Los Lagos"),
            ("Aysén del General Carlos Ibáñez del Campo", "Aysén del General Carlos Ibáñez del Campo"),
            ("Magallanes y de la Antártica Chilena", "Magallanes y de la Antártica Chilena")
        ], 
        default="Metropolitana de Santiago"
    )
    estado_suscripcion = models.CharField(max_length=10, choices=[('activa', 'Activa'), ('desactiva', 'Desactiva')])
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Tiendas'


class UsuarioTienda(models.Model):
    id_usuario_tienda = models.AutoField(primary_key=True)
    id_tienda = models.ForeignKey(Tiendas, on_delete=models.CASCADE)
    id_rol = models.ForeignKey(RolUsuario, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Usuario_Tienda'


class Ventas(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    id_usuario_tienda = models.ForeignKey(UsuarioTienda, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Ventas'


class Productos(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=10, choices=[('arriendo', 'Arriendo'), ('venta', 'Venta')])

    class Meta:
        db_table = 'Productos'


class InventarioArriendo(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=25, null=True, blank=True)
    id_tienda = models.ForeignKey(Tiendas, null=True, blank=True, on_delete=models.CASCADE)
    precio_arriendo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cantidad_disponible = models.IntegerField()
    talla_producto = models.CharField(
        max_length=10,
        choices=[
            ("XS", "XS"), ("S", "S"), ("M", "M"), ("L", "L"), ("XL", "XL"), ("XXL", "XXL"),
            ("35", "35"), ("36", "36"), ("37", "37"), ("38", "38"), ("39", "39"),
            ("40", "40"), ("41", "41"), ("42", "42"), ("43", "43"), ("44", "44"), ("45", "45")
        ],
        default="45"
    )

    class Meta:
        db_table = 'InventarioArriendo'


class DetalleArriendo(models.Model):
    id_detallea = models.AutoField(primary_key=True)
    id_arriendo = models.ForeignKey('Arriendos', on_delete=models.CASCADE)
    id_producto = models.ForeignKey(InventarioArriendo, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'Detalle_Arriendo'


class Arriendos(models.Model):
    id_arriendo = models.AutoField(primary_key=True)
    fecha_arriendo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    id_usuario_tienda = models.ForeignKey(UsuarioTienda, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Arriendos'


class DetallesVenta(models.Model):
    id_detallev = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    id_producto = models.ForeignKey('Inventario', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'Detalles_Venta'


class Suscripcion(models.Model):
    id_sub = models.AutoField(primary_key=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    id_tienda = models.ForeignKey(Tiendas, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Suscripcion'


class Inventario(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=25, null=True, blank=True)
    id_tienda = models.ForeignKey(Tiendas, null=True, blank=True, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cantidad_disponible = models.IntegerField()
    talla_producto = models.CharField(
        max_length=10,
        choices=[
            ("XS", "XS"), ("S", "S"), ("M", "M"), ("L", "L"), ("XL", "XL"), ("XXL", "XXL"),
            ("35", "35"), ("36", "36"), ("37", "37"), ("38", "38"), ("39", "39"),
            ("40", "40"), ("41", "41"), ("42", "42"), ("43", "43"), ("44", "44"), ("45", "45")
        ],
        default="45"
    )

    class Meta:
        db_table = 'Inventario'


####PAULA MIKAL INICIO####

class SolicitudLocal(models.Model):
    nombre_local = models.CharField(max_length=50)
    patente = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_local

    class Meta:
        db_table = 'solicitud_local'


class SolicitudUsuario(models.Model):
    id_solicitud_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    telefono = models.IntegerField()
    correo = models.EmailField(max_length=100)
    contraseña = models.CharField(max_length=225)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'solicitud_usuario'

    def save(self, *args, **kwargs):
        # Hashear la contraseña antes de guardar el objeto
        if self.contraseña:
            self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)


class Registrarme(models.Model):
    nombre = models.CharField(max_length=25)
    telefono = models.CharField(max_length=9)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=25)  # Contraseña en texto plano

    def save(self, *args, **kwargs):
        # No hashear la contraseña, se guarda tal cual
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'registrarme'
###paula fin###

class CarritoDeCompras(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    tienda_id = models.IntegerField() 
    producto_id = models.IntegerField()  # ID del producto añadido.
    nombre_producto = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.precio * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Carrito de {self.usuario} - {self.nombre_producto} ({self.cantidad})"

    class Meta:
        verbose_name_plural = "Carritos de Compras"


class CarritoDeArriendo(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    tienda_id = models.IntegerField()
    producto_id = models.IntegerField()  # ID del producto arrendado.
    nombre_producto = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.precio * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Carrito de Arriendo de {self.usuario} - {self.nombre_producto} ({self.cantidad})"

    class Meta:
        verbose_name_plural = "Carritos de Arriendo"
