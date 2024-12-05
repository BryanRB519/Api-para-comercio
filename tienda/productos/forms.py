from django import forms
from .models import Producto

class VentaForm(forms.Form):
    # Campo para ingresar el código de barras
    codigo_barras = forms.CharField(max_length=100, required=True, label="Código de barras")
    
    # Campo para ingresar la cantidad de productos
    cantidad = forms.IntegerField(min_value=1, initial=1, required=True, label="Cantidad")
    
    # Método para validar si el código de barras corresponde a un producto en la base de datos
    def clean_codigo_barras(self):
        codigo_barras = self.cleaned_data.get('codigo_barras')
        
        # Verificar si el producto con el código de barras existe
        try:
            producto = Producto.objects.get(codigo_barras=codigo_barras)
        except Producto.DoesNotExist:
            raise forms.ValidationError("Producto no encontrado.")
        
        return codigo_barras

    # Método para validar si la cantidad es suficiente en stock
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        codigo_barras = self.cleaned_data.get('codigo_barras')
        
        # Buscar el producto con el código de barras
        producto = Producto.objects.get(codigo_barras=codigo_barras)
        
        # Verificar si hay suficiente stock
        if producto.stock < cantidad:
            raise forms.ValidationError("No hay suficiente stock para esta cantidad.")
        
        return cantidad
