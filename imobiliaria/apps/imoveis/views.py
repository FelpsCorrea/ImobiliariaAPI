from rest_framework import viewsets
from .models import Imovel
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

'''
    CRUD de Imóvel
'''
class ImovelViewSet(viewsets.ModelViewSet):
    
    # Definindo a classe de autenticação
    authentication_classes = [JWTAuthentication]

    # Somente usuários autenticados podem acessar os métodos da ImovelViewSet
    permission_classes = [IsAuthenticated]
    
    # Definição dos métodos disponíveis    
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    '''
        Definição do queryset para considerar que os que tenham ativo=0 "não existem"
    '''
    def get_queryset(self):
        return Imovel.objects.filter(ativo=True)
    
    '''
        Definição dos serializers para cada método da VIEW
    '''
    def get_serializer_class(self):
        if self.action == 'create':
            return ImovelCreateSerializer
        return ImovelSerializer  # caso contrário, o padrão é usado