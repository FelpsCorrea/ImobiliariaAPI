from rest_framework import viewsets
from .models import Imovel
from .serializers import *

class ImovelViewSet(viewsets.ModelViewSet):
    
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