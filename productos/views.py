from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
import pandas as pd
from .models import Producto, Mascota, Cliente, Consulta
from .serializers import ProductoSerializer, MascotaSerializer, ClienteSerializer, ConsultaSerializer

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

# Vista de consultas
class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='exportar-excel')
    def exportar_excel(self, request):
        consultas = Consulta.objects.all()
        data = [
            {
                'ID': consulta.id,
                'Fecha': consulta.fecha_consulta,
                'Hora': consulta.hora,
                'Mascota': consulta.mascota.nombre,
                'Cliente': consulta.cliente.nombre,
                'Motivo': consulta.motivo,
                'Observación': consulta.observacion,
            }
            for consulta in consultas
        ]
        
        # Crear DataFrame de pandas
        df = pd.DataFrame(data)
        
        # Crear respuesta con archivo Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=consultas.xlsx'
        
        # Escribir el DataFrame al archivo Excel en la respuesta
        with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Consultas')
        
        return response
