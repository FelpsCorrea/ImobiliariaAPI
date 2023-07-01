from rest_framework import viewsets
from .models import Reserva
from .serializers import *

class ReservaViewSet(viewsets.ModelViewSet):
    
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