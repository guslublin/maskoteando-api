from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    costo = models.IntegerField(null=True, blank=True)  # Cambiado a IntegerField
    precio_venta = models.IntegerField(null=True, blank=True)  # Cambiado a IntegerField
    stock = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    ci = models.PositiveIntegerField()  # CI como número positivo
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=255)
    barrio = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    observacion = models.TextField(blank=True, null=True)  # Observación puede ser opcional

    def __str__(self):
        return self.nombre

class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    raza = models.CharField(max_length=100)
    procedencia = models.CharField(max_length=100)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='mascotas')  # Relacion con Cliente

    def __str__(self):
        return self.nombre
    
class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, blank=True)  # Relación con productos
    mascotas = models.ManyToManyField(Mascota, blank=True)  # Relación con mascotas
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta {self.id} - {self.cliente.nombre}"