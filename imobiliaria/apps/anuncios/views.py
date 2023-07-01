from rest_framework import viewsets
from .models import Anuncio
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

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
        return AnuncioSerializer  # caso contrário, o padrão é usado

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