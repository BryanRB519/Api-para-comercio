from .models import*
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class RegistrarVenta(APIView):
    def post(self, request):
        data = request.data
        codigo_barras = data.get('codigo_barras')
        cantidad = data.get('cantidad', 1)

        try:
            producto = Producto.objects.get(codigo_barras=codigo_barras)

            if producto.stock < int(cantidad):
                return Response(
                    {"error": "Stock insuficiente para realizar la venta."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            venta = Venta.objects.create(
                producto=producto,
                cantidad=cantidad,
            )
            return Response(
                {"mensaje": f"Venta registrada: {venta.cantidad}x {venta.producto.nombre}. Stock restante: {producto.producto.stock}."},
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
