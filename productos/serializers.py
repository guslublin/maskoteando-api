from rest_framework import serializers
from .models import Producto, Mascota, Cliente, Venta

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'ci', 'fecha_nacimiento', 'direccion', 'barrio', 'ciudad', 'observacion']

class MascotaSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())  # Relación con Cliente

    class Meta:
        model = Mascota
        fields = ['id', 'nombre', 'fecha_nacimiento', 'raza', 'procedencia', 'cliente']

class VentaSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer()
    productos = ProductoSerializer(many=True)
    mascotas = MascotaSerializer(many=True)

    class Meta:
        model = Venta
        fields = ['id', 'cliente', 'productos', 'mascotas', 'total', 'fecha']