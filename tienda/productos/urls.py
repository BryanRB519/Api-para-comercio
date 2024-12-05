from django.contrib import admin
from django.urls import path, include
from productos.views import RegistrarVenta  # Asegúrate de importar la vista correctamente

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RegistrarVenta.as_view(), name='registrar_venta'),  # Esta ruta es para la URL raíz
    path('api/registrar-venta/', RegistrarVenta.as_view(), name='registrar_venta'),  # Ruta para API
    path('productos/', include('productos.urls')),
]
