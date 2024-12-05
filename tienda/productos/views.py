from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Producto, Venta, DetalleVenta

class RegistrarVenta(APIView):
    def post(self, request):
        data = request.data
        codigo_barras = data.get('codigo_barras')
        cantidad = int(data.get('cantidad', 1))  # Convierte a entero

        try:
            # Buscar el producto por el código de barras
            producto = Producto.objects.get(codigo_barras=codigo_barras)

            # Verificar si hay suficiente stock
            if producto.stock < cantidad:
                return Response(
                    {"error": "Stock insuficiente para realizar la venta."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Crear la venta
            venta = Venta.objects.create()

            # Crear el detalle de la venta y descontar del stock
            detalle = DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                total=producto.precio_venta * cantidad
            )

            # Actualizar el stock del producto
            producto.stock -= cantidad
            producto.save()

            return Response(
                {
                    "mensaje": f"Venta registrada: {detalle.cantidad}x {detalle.producto.nombre}. Stock restante: {producto.stock}.",
                    "venta_id": venta.id
                },
                status=status.HTTP_201_CREATED
            )

        except Producto.DoesNotExist:
            return Response(
                {"error": "Producto no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Error al registrar la venta: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
