from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny  # Importa AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Producto, Mascota, Cliente, Venta
from .serializers import ProductoSerializer, MascotaSerializer, ClienteSerializer, VentaSerializer
from rest_framework.permissions import IsAuthenticated

# Registro de usuarios
@api_view(['POST'])
@permission_classes([AllowAny])  # Permitir acceso a cualquier usuario
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'detail': 'El usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    
    refresh = RefreshToken.for_user(user)

    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }, status=status.HTTP_201_CREATED)


# Vista de productos
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

# Vista de mascotas
class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer

# Vista de clientes
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

@api_view(['POST'])
def crear_venta(request):
    cliente_id = request.data.get('cliente')
    productos_ids = request.data.get('productos', [])
    mascotas_ids = request.data.get('mascotas', [])

    try:
        cliente = Cliente.objects.get(id=cliente_id)
        productos = Producto.objects.filter(id__in=productos_ids)
        mascotas = Mascota.objects.filter(id__in=mascotas_ids)
    except (Cliente.DoesNotExist, Producto.DoesNotExist, Mascota.DoesNotExist) as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Calcular total
    total = sum([producto.precio_venta for producto in productos]) + sum([mascota.precio for mascota in mascotas])

    venta = Venta.objects.create(cliente=cliente, total=total)
    venta.productos.set(productos)
    venta.mascotas.set(mascotas)
    venta.save()

    return Response(VentaSerializer(venta).data, status=status.HTTP_201_CREATED)