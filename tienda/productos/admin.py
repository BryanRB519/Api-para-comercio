from django.contrib import admin
from .models import Categoria, Producto, Venta, DetalleVenta


### CONFIGURACIÓN DEL PANEL DE ADMINISTRACIÓN ###

# Configuración del modelo Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """
    Configuración del panel para gestionar categorías de productos.
    """
    list_display = ('nombre', 'descripcion')  # Columnas visibles en la lista
    search_fields = ('nombre',)  # Permite buscar categorías por nombre
    ordering = ('nombre',)  # Ordena las categorías alfabéticamente


# Configuración del modelo Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """
    Configuración del panel para gestionar productos.
    """
    list_display = (
        'nombre', 
        'categoria', 
        'codigo_barras', 
        'stock', 
        'precio_compra', 
        'precio_venta', 
        'actualizado'
    )
    list_filter = ('categoria',)  # Filtro lateral por categoría
    search_fields = ('nombre', 'codigo_barras')  # Búsqueda por nombre o código de barras
    ordering = ('-actualizado',)  # Ordena por fecha de actualización más reciente
    readonly_fields = ('actualizado', 'creado')  # Campos solo lectura en el formulario
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'categoria', 'codigo_barras', 'stock')
        }),
        ('Precios', {
            'fields': ('precio_compra', 'precio_venta'),
        }),
        ('Tiempos', {
            'fields': ('creado', 'actualizado'),
        }),
    )  # Agrupación de campos en secciones


# Configuración del modelo DetalleVenta como inline
class DetalleVentaInline(admin.TabularInline):
    """
    Configuración inline para gestionar los productos asociados a una venta.
    """
    model = DetalleVenta
    extra = 1  # Una fila adicional para agregar productos fácilmente
    fields = ('producto', 'cantidad', 'total')  # Campos mostrados en el inline
    readonly_fields = ('total',)  # Campo de solo lectura para evitar errores
    verbose_name = "Producto en la Venta"
    verbose_name_plural = "Productos en la Venta"


# Configuración del modelo Venta
@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    """
    Configuración del panel para gestionar ventas.
    """
    list_display = ('id', 'mostrar_total', 'fecha')  # Columnas visibles en la lista
    list_filter = ('fecha',)  # Filtro lateral por fecha
    search_fields = ('id',)  # Búsqueda por ID de venta
    ordering = ('-fecha',)  # Ordena por la fecha más reciente
    inlines = [DetalleVentaInline]  # Relaciona detalles de venta directamente en el formulario

    def mostrar_total(self, obj):
        """
        Calcula el total de la venta y lo muestra en formato profesional.
        """
        return f"${obj.calcular_total():,.2f}"  # Formato con comas y dos decimales
    mostrar_total.short_description = "Total de la Venta"  # Título de la columna
    mostrar_total.admin_order_field = 'fecha'  # Ordena la columna por fecha


# Configuración del modelo DetalleVenta
@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    """
    Configuración del panel para gestionar los productos de una venta.
    """
    list_display = ('venta', 'producto', 'cantidad', 'total')  # Columnas visibles en la lista
    list_filter = ('producto', 'venta')  # Filtro lateral por producto o venta
    search_fields = ('producto__nombre', 'venta__id')  # Búsqueda por nombre de producto o ID de venta
    readonly_fields = ('total',)  # Campo total como solo lectura
    ordering = ('-venta',)  # Ordena por ventas más recientes


### MEJORAS Y CLARIDAD ###

"""
1. **Campos Agrupados:** Los campos en el modelo `Producto` están organizados en secciones 
   para mejorar la claridad y profesionalismo.
2. **Detalles de Venta Inline:** Ahora puedes gestionar productos asociados a una venta directamente 
   desde la pantalla de edición de ventas, sin necesidad de salir.
3. **Formato Profesional:** Totales formateados con separadores de miles y decimales.
4. **Comentarios y Documentación:** Agregué comentarios detallados y docstrings para facilitar la comprensión del código.
5. **Filtros y Búsqueda Avanzados:** Los modelos incluyen opciones de búsqueda y filtrado específicas 
   para mejorar la experiencia del cliente.
"""
