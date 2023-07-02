from rest_framework import serializers
from .models import Reserva
from apps.anuncios.serializers import AnuncioSerializer
from apps.anuncios.models import Anuncio
from django.utils import timezone
from django.db.models import Q
from apps.imoveis.models import Imovel

'''
    Serializer responsável por validar os parâmetreos para o CREATE
'''
class ReservaCreateSerializer(serializers.ModelSerializer):
    
    # Validação do anuncio vinculado à reserva
    anuncio_id = serializers.PrimaryKeyRelatedField(
        required=True, 
        queryset=Anuncio.objects.filter(ativo=True), # Para validar que seja um id existente
        error_messages={
            'required': 'Por favor, forneça o ID do anúncio que a reserva é vinculada.',
            'does_not_exist': 'O anúncio especificado não existe.'
        },
        write_only=True,
        source='anuncio'  # Indica que este campo é usado como a fonte para o campo 'anuncio' do modelo
    )
    
    comentario = serializers.CharField(required=False, error_messages={
        'blank': 'O comentário não pode estar em branco',
        'invalid': 'O comentário deve ser uma string.'
    })
    
    valor_total = serializers.FloatField(required=False, min_value=0, error_messages={
        'invalid': 'O valor total deve ser um valor válido.'
    })
    
    data_checkin = serializers.DateField()
    
    data_checkout = serializers.DateField()
    
    # Verifica se a data de checkin fornecida é maior ou igual que a data atual.
    def validate_data_checkin(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("A data de checkin não pode ser no passado.")
        return value
    
    # Verifica se a data de checkout fornecida é maior ou igual que a data atual.
    def validate_data_checkout(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("A data de checkout não pode ser no passado.")
        return value
    
    # Função executada implicitamente, mas é possível fazer validações personalizadas dentro dela.
    def validate(self, attrs):
        
        # Valida se a data de checkin é menor que a data de checkout
        if attrs['data_checkin'] > attrs['data_checkout']:
            raise serializers.ValidationError("A data de check-in não pode ser superior à data de check-out.")

        # Existem 3 possíveis cenários para uma reserva conflitar, 
        # basicamente pensando checkin - checkout como uma linha, esses 3 casos são de linhas que estariam sobrepostas
        # checkout > input_checkin AND checkout < input_checkout
        # checkin > input_checkin AND checkout < input_checkout
        # checkin < input_checkout AND checkin > input_checkin
        
        # Primeiro filtra todas reservas do mesmo imóvel
        # Após filtrar todas as reservas do mesmo imóvel, filtra as reservas que conflitam conforme as regras acima
        # O operador "Q" permite fazer consultas complexas
        # gt=Maior que, gte=Maior ou igual que, lt=Menor que, lte=Menor ou igual que
        if 'anuncio' in attrs and Reserva.objects.filter(anuncio__imovel=attrs['anuncio'].imovel).filter(
            (
                Q(data_checkout__gt=attrs['data_checkin'], data_checkout__lte=attrs['data_checkout']) |
                Q(data_checkin__gte=attrs['data_checkin'], data_checkin__lt=attrs['data_checkout']) |
                Q(data_checkin__lte=attrs['data_checkin'], data_checkout__gte=attrs['data_checkout'])
            )
            ).exists():
            raise serializers.ValidationError("A reserva conflita com uma reserva existente para o mesmo imóvel.")

        return attrs
    
    anuncio = AnuncioSerializer(many=False, required=False)

    class Meta:
        model = Reserva
        fields = '__all__' # Retorna todos dados da tabela
        read_only_fields = ('id', 'data_criacao', 'data_hora_atualizacao', 'anuncio', 'codigo') # Define que esses campos não serão incluídos na criação
        
'''
    Serializer responsável por retornar os dados para os métodos GET
'''
class ReservaSerializer(serializers.ModelSerializer):
    
    anuncio = AnuncioSerializer(many=False, required=False)

    class Meta:
        model = Reserva
        fields = '__all__' # Retorna todos dados da tabela
        
'''
    By Imovel Serializer (validar parâmetros)
'''
class ImovelIdSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        required=True, 
        queryset=Imovel.objects.filter(ativo=True), # Para validar que seja um id existente
        error_messages={
            'required': 'Por favor, forneça o ID do imóvel que deseja listar as reservas.',
            'does_not_exist': 'O imóvel especificado não existe'
        }
    )
    
'''
    By Anuncio Serializer (validar parâmetros)
'''
class AnuncioIdSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        required=True, 
        queryset=Anuncio.objects.filter(ativo=True), # Para validar que seja um id existente
        error_messages={
            'required': 'Por favor, forneça o ID do anúncio que deseja listar as reservas.',
            'does_not_exist': 'O anúncio especificado não existe'
        }
    )