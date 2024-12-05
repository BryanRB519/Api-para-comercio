# urls.py
from django.urls import path
from .views import RegistrarVenta

urlpatterns = [
    path('api/registrar-venta/', RegistrarVenta.as_view(), name='registrar_venta'),
]
