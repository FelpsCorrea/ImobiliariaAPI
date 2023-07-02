from rest_framework import viewsets
from .models import Reserva
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

'''
    CRUD de Reserva, sem incluir PUT ou PATCH
'''
class ReservaViewSet(viewsets.ModelViewSet):
    
    # Definindo a classe de autenticação
    authentication_classes = [JWTAuthentication]

    # Somente usuários autenticados podem acessar os métodos da ReservaViewSet
    permission_classes = [IsAuthenticated]
    
    # Definição dos métodos disponíveis    
    http_method_names = ['get', 'post', 'delete']
    
    '''
        Definição do queryset para considerar que os que tenham ativo=0 "não existem"
    '''
    def get_queryset(self):
        return Reserva.objects.filter(ativo=True)
    
    '''
        Definição dos serializers para cada método da VIEW
    '''
    def get_serializer_class(self):
        if self.action == 'create':
            return ReservaCreateSerializer
        return ReservaSerializer  # caso contrário, o padrão é usado
    
    '''
        View referente a listagem de reservas a partir de um imóvel
    '''    
    @action(detail=False, methods=['GET'], url_path='byimovel/(?P<id_imovel>[^/.]+)', url_name='reserva_byimovel')
    def by_imovel(self, request, id_imovel=None):
        
        # Usa o Serializer para validar a entrada
        serializer = ImovelIdSerializer(data={'id': id_imovel})
        serializer.is_valid(raise_exception=True)
        
        # Busca as reservas pertencentes ao imóvel
        id_imovel = serializer.validated_data['id']
        reservas = Reserva.objects.filter(anuncio__imovel_id=id_imovel)
        
        # Serializa os dados para retornar
        serializer = ReservaSerializer(reservas, many=True)
        
        return Response(serializer.data)
    
    '''
        View referente a listagem de reservas a partir de um anúncio
    '''    
    @action(detail=False, methods=['GET'], url_path='byanuncio/(?P<id_anuncio>[^/.]+)', url_name='reserva_byanuncio')
    def by_anuncio(self, request, id_anuncio=None):
        
        # Usa o Serializer para validar a entrada
        serializer = AnuncioIdSerializer(data={'id': id_anuncio})
        serializer.is_valid(raise_exception=True)
        
        # Busca as reservas pertencentes ao anuncio
        id_anuncio = serializer.validated_data['id']
        reservas = Reserva.objects.filter(anuncio_id=id_anuncio)
        
        # Serializa os dados para retornar
        serializer = ReservaSerializer(reservas, many=True)
        
        return Response(serializer.data)