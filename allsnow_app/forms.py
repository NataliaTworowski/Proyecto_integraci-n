from django import forms
from .models import SolicitudUsuario, SolicitudLocal, Registrarme
from .models import Inventario
from .models import InventarioArriendo


####PAULA MIKAL INICIO####

class SolicitudUsuarioForm(forms.ModelForm):
    class Meta:
        model = SolicitudUsuario
        fields = ['nombre', 'apellido', 'rut', 'telefono', 'correo', 'contraseña']
        widgets = {
            'contraseña': forms.PasswordInput(),
        }


class SolicitudLocalForm(forms.ModelForm):
    REGION_CHOICES = [
        ('Arica y Parinacota', 'Arica y Parinacota'),
        ('Tarapacá', 'Tarapacá'),
        ('Antofagasta', 'Antofagasta'),
        ('Atacama', 'Atacama'),
        ('Coquimbo', 'Coquimbo'),
        ('Valparaíso', 'Valparaíso'),
        ('Metropolitana de Santiago', 'Metropolitana de Santiago'),
        ('O’Higgins', 'O’Higgins'),
        ('Maule', 'Maule'),
        ('Ñuble', 'Ñuble'),
        ('Biobío', 'Biobío'),
        ('La Araucanía', 'La Araucanía'),
        ('Los Ríos', 'Los Ríos'),
        ('Los Lagos', 'Los Lagos'),
        ('Aysén', 'Aysén'),
        ('Magallanes', 'Magallanes'),
    ]

    ubicacion = forms.ChoiceField(choices=REGION_CHOICES)

    class Meta:
        model = SolicitudLocal
        fields = ['nombre_local', 'patente', 'ubicacion']



class RegistrarmeForm(forms.ModelForm):
    class Meta:
        model = Registrarme
        fields = ['nombre', 'telefono', 'correo', 'contraseña']
        widgets = {
            'contraseña': forms.PasswordInput(), } 
        
class LoginForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña', max_length=25)

####PAULA MIKAL FIN####




class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['nombre_producto', 'precio', 'cantidad_disponible', 'talla_producto']  # Cambia los campos según tu modelo
        labels = {
            'nombre_producto : nombre'
            'precio': 'Precio (CLP)', 
            'cantidad_disponible': 'Cantidad',
            'talla_producto': 'Talla',
        }
        widgets = {
            'precio': forms.NumberInput(attrs={
                'class': 'form-control', 
                'id': 'precio', 
                'step': '500',  
                'placeholder': 'Ingrese el precio en CLP'  
            }),
            'cantidad_disponible': forms.NumberInput(attrs={
                'class': 'form-control', 
                'id': 'cantidadDisponible'
            }),
            'talla_producto': forms.Select(attrs={'class': 'form-control', 'id': 'tallaProducto'}),  
        }

class InventarioArriendoForm(forms.ModelForm):
    class Meta:
        model = InventarioArriendo
        fields = ['nombre_producto', 'cantidad_disponible', 'talla_producto', 'precio_arriendo']
        labels = {
            'nombre_producto': 'Nombre',  
            'cantidad_disponible': 'Cantidad',
            'talla_producto': 'Talla',
            'precio_arriendo': 'Precio de Arriendo (CLP)',
        }
        widgets = {
            'precio_arriendo': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'precioArriendo',
                'step': '500',  
                'placeholder': 'Ingrese el precio de arriendo en CLP'  
            }),
            'cantidad_disponible': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'cantidadDisponible'
            }),
            'talla_producto': forms.Select(attrs={'class': 'form-control', 'id': 'talla_producto'}),
        }
        
####################NATY######################3
from allsnow_app.models import Tiendas

class TiendaForm(forms.ModelForm):
    class Meta:
        model = Tiendas
        fields = ['descripcion'] 