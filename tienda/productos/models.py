from django.db import models
from django.utils.timezone import now

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='productos')
    codigo_barras = models.CharField(max_length=50, unique=True)
    stock = models.PositiveIntegerField(default=0)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def vender(self, cantidad=1):
        if self.stock >= cantidad:
            self.stock -= cantidad
            self.save()
        else:
            raise ValueError(f"Stock insuficiente para {self.nombre}.")

    def __str__(self):
        return self.nombre


class Venta(models.Model):
    fecha = models.DateTimeField(default=now)

    def calcular_total(self):
        return sum(detalle.total for detalle in self.detalles.all())

    def __str__(self):
        return f"Venta #{self.id} - Total: {self.calcular_total():.2f} pesos"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='detalles_venta')
    cantidad = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total = self.cantidad * self.producto.precio_venta
        self.producto.vender(self.cantidad)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} - {self.total:.2f} pesos"
