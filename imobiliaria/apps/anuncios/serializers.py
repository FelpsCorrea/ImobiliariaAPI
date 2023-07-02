from rest_framework import serializers
from .models import Anuncio, PlataformaAnuncio
from apps.imoveis.serializers import ImovelSerializer
from apps.imoveis.models import Imovel

'''
    Serializer para as plataformas do anúncio
'''
class PlataformaAnuncioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PlataformaAnuncio
        fields = '__all__' # Retorna todos dados da tabela

'''
    Serializer responsável por validar os parâmetreos para o CREATE
'''
class AnuncioCreateSerializer(serializers.ModelSerializer):
    
    # Validação do imóvel informado na criação do anúncio
    imovel_id = serializers.PrimaryKeyRelatedField(
        required=True, 
        queryset=Imovel.objects.filter(ativo=True), # Para validar que seja um id existente
        error_messages={
            'required': 'Por favor, forneça o ID do imóvel que o anúncio pertence.',
            'does_not_exist': 'O imóvel especificado não existe'
        },
        write_only=True,
        source='imovel'  # Indica que este campo é usado como a fonte para o campo 'anuncio' do modelo
    )
    
    # Validação da plataforma informado na criação do anúncio
    plataforma_id = serializers.PrimaryKeyRelatedField(
        required=True, 
        queryset=PlataformaAnuncio.objects.filter(ativo=True), # Para validar que seja um id existente
        error_messages={
            'required': 'Por favor, forneça o ID da plataforma que o anúncio foi publicado.',
            'does_not_exist': 'A plataforma especificada não existe'
        },
        write_only=True,
        source='plataforma'  # Indica que este campo é usado como a fonte para o campo 'plataforma' do modelo
    )
    
    # Formatação do imóvel e da plataforma a serem retornados
    imovel = ImovelSerializer(many=False, required=False)
    plataforma = PlataformaAnuncioSerializer(many=False, required=False)

    class Meta:
        model = Anuncio
        fields = '__all__' # Retorna todos dados da tabela
        read_only_fields = ('id', 'data_criacao', 'data_hora_atualizacao') # Define que esses campos não serão incluídos na criação 
        
'''
    Serializer responsável por validar os parâmetros do PARTIAL_UPDATE e retornar os dados para os métodos GET
'''
class AnuncioSerializer(serializers.ModelSerializer):
    
    # Validação da plataforma informado no update do anúncio
    plataforma_id = serializers.PrimaryKeyRelatedField(
        required=False, 
        queryset=PlataformaAnuncio.objects.filter(ativo=True), # Para validar que seja um id existente
        error_messages={
            'required': 'Por favor, forneça o ID da plataforma que o anúncio foi publicado.',
            'does_not_exist': 'A plataforma especificada não existe'
        },
        write_only=True,
        source='plataforma'  # Indica que este campo é usado como a fonte para o campo 'plataforma' do modelo
    )
    
    # Formatação do imóvel e da plataforma a serem retornados
    imovel = ImovelSerializer(many=False, required=False)
    plataforma = PlataformaAnuncioSerializer(many=False, required=False)

    class Meta:
        model = Anuncio
        fields = '__all__' # Retorna todos dados da tabela
        read_only_fields = ('id', 'data_criacao', 'data_hora_atualizacao', 'imovel') # Define que esses campos não serão incluídos na criação
        
'''
    By Imovel Serializer (validar parâmetros)
'''
class ImovelIdSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        required=True, 
        queryset=Imovel.objects.filter(ativo=True), # Para validar que seja um id existente
        error_messages={
            'required': 'Por favor, forneça o ID do imóvel que deseja listar os anuncios.',
            'does_not_exist': 'O imóvel especificado não existe'
        }
    )