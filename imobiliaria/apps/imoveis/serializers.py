from rest_framework import serializers
from .models import Imovel
from django.utils import timezone

'''
    Serializer responsável por validar os parâmetreos para o CREATE
'''
class ImovelCreateSerializer(serializers.ModelSerializer):
    
    limite_hospedes = serializers.IntegerField(required=True, min_value=1, error_messages={
        'required': 'Por favor, forneça o número de hóspedes.',
        'min_value': 'O número de hóspedes deve ser um número inteiro válido.',
        'invalid': 'O número de hóspedes deve ser um número inteiro válido.'
    })
    
    quant_banheiros = serializers.IntegerField(required=False, min_value=0, error_messages={
        'invalid': 'O número de banheiros deve ser um número inteiro válido.',
        'min_value': 'O número de banheiros deve ser um número inteiro válido.'
    })
    
    aceita_animais = serializers.BooleanField(required=False, error_messages={
        'invalid': 'O valor para aceita_animais deve ser um booleano'
    })
    
    valor_limpeza = serializers.FloatField(required=False, min_value=0, error_messages={
        'invalid': 'O valor da limpeza deve ser um valor válido.'
    })
    
    data_ativacao = serializers.DateField(required=False)
    
    def validate_data_ativacao(self, value):
        """
        Verifica se a data de ativação fornecida é maior ou igual que a data atual.
        """
        if value < timezone.now().date():
            raise serializers.ValidationError("A data de ativação não pode ser no passado.")
        return value

    class Meta:
        model = Imovel
        fields = '__all__' # Retorna todos dados da tabela
        read_only_fields = ('id', 'data_criacao', 'data_hora_atualizacao') # Define que esses campos não serão incluídos na criação
        
'''
    Serializer responsável por validar os parâmetros do PARTIAL_UPDATE e retornar os dados para os métodos GET
'''
class ImovelSerializer(serializers.ModelSerializer):
    
    limite_hospedes = serializers.IntegerField(required=False, min_value=1, error_messages={
        'required': 'Por favor, forneça o número de hóspedes.',
        'min_value': 'O número de hóspedes deve ser um número inteiro válido.',
        'invalid': 'O número de hóspedes deve ser um número inteiro válido.'
    })
    
    quant_banheiros = serializers.IntegerField(required=False, min_value=0, error_messages={
        'invalid': 'O número de banheiros deve ser um número inteiro válido.',
        'min_value': 'O número de banheiros deve ser um número inteiro válido.'
    })
    
    aceita_animais = serializers.BooleanField(required=False, error_messages={
        'invalid': 'O valor para aceita_animais deve ser um booleano'
    })
    
    valor_limpeza = serializers.FloatField(required=False, min_value=0, error_messages={
        'invalid': 'O valor da limpeza deve ser um valor válido.'
    })
    
    data_ativacao = serializers.DateField(required=False)
    
    def validate_data_ativacao(self, value):
        """
        Verifica se a data de ativação fornecida é maior ou igual que a data/hora atual.
        """
        if value < timezone.now().date():
            raise serializers.ValidationError("A data de ativação não pode ser no passado.")
        return value

    class Meta:
        model = Imovel
        fields = '__all__' # Retorna todos dados da tabela   
        read_only_fields = ('id', 'data_criacao', 'data_hora_atualizacao') # Define que esses campos não serão incluídos na criação 