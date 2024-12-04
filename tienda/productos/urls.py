from django.urls import path
from .views import RegistrarVenta

urlpatterns = [
    path('api/productos/vender/', RegistrarVenta.as_view(), name='registrar_venta'),
]

