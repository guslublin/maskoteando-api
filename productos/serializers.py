from rest_framework import serializers
from .models import Producto, Mascota, Cliente, Consulta

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

class ConsultaSerializer(serializers.ModelSerializer):
    mascota_nombre = serializers.CharField(source='mascota.nombre', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)

    class Meta:
        model = Consulta
        fields = ['id', 'fecha_consulta', 'hora', 'motivo', 'observacion', 'mascota', 'cliente', 'mascota_nombre', 'cliente_nombre']