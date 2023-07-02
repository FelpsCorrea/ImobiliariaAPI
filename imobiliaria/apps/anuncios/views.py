from rest_framework import viewsets
from .models import Anuncio
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

'''
    CRUD de anúncio, sem incluir DELETE
'''
class AnuncioViewSet(viewsets.ModelViewSet):
    
    # Definindo a classe de autenticação
    authentication_classes = [JWTAuthentication]

    # Somente usuários autenticados podem acessar os métodos da AnuncioViewSet
    permission_classes = [IsAuthenticated]
    
    # Definição dos métodos disponíveis
    http_method_names = ['get', 'post', 'patch']
    
    '''
        Definição do queryset para considerar que os que tenham ativo=0 "não existem"
    '''
    def get_queryset(self):
        return Anuncio.objects.filter(ativo=True)
    
    '''
        Definição dos serializers para cada método da VIEW
    '''
    def get_serializer_class(self):
        if self.action == 'create':
            return AnuncioCreateSerializer
        return AnuncioSerializer  # caso contrário, o padrão é 
    
    '''
        View referente a listagem de anúncios a partir de um imóvel
    '''    
    @action(detail=False, methods=['GET'], url_path='byimovel/(?P<id_imovel>[^/.]+)', url_name='anuncio_byimovel')
    def by_imovel(self, request, id_imovel=None):
        
        # Usa o Serializer para validar a entrada
        serializer = ImovelIdSerializer(data={'id': id_imovel})
        serializer.is_valid(raise_exception=True)
        
        # Busca os anúncios pertencentes ao imóvel
        id_imovel = serializer.validated_data['id']
        anuncios = Anuncio.objects.filter(imovel_id=id_imovel)
        
        # Serializa os dados para retornar
        serializer = AnuncioSerializer(anuncios, many=True)
        
        return Response(serializer.data)

'''
    GET das plataformas
'''
class PlataformaAnuncioViewSet(viewsets.ModelViewSet):
    
    # Definindo a classe de autenticação
    authentication_classes = [JWTAuthentication]

    # Somente usuários autenticados podem acessar os métodos da PlataformaAnuncioViewSet
    permission_classes = [IsAuthenticated]
    
    http_method_names = ['get']
    
    '''
        Definição do queryset para considerar que os que tenham ativo=0 "não existem"
    '''
    def get_queryset(self):
        return PlataformaAnuncio.objects.filter(ativo=True)
    
    '''
        Definição dos serializers para cada método da VIEW
    '''
    def get_serializer_class(self):
        return PlataformaAnuncioSerializer