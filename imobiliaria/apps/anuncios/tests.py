from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from apps.imoveis.models import Imovel
from .models import Anuncio, PlataformaAnuncio

class AnuncioApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Cria 1 imóvel fictício
        self.imovel = Imovel.objects.create(
            limite_hospedes=2,
            aceita_animais=True,
            valor_limpeza=100,
            data_ativacao=timezone.now().date()
        )
    
        # Cria 2 plataformas fictícias
        self.plataforma_anuncio1 = PlataformaAnuncio.objects.create(
            taxa=50,
            nome="Airbnb"
        )
        
        self.plataforma_anuncio2 = PlataformaAnuncio.objects.create(
            taxa=60,
            nome="Hurb"
        )
        
        # Cria 2 anúncios fictícios vinculados ao imóvel
        self.anuncio1 = Anuncio.objects.create(
            imovel=self.imovel,
            plataforma=self.plataforma_anuncio1
        )
        self.anuncio2 = Anuncio.objects.create(
            imovel=self.imovel,
            plataforma=self.plataforma_anuncio1
        )

    '''
        Teste que verifica se está funcionando a busca por um anúncio por seu id
    '''
    def test_get_single_anuncio(self):

        # Faz uma requisição GET para o endpoint
        url = reverse('anuncio-detail', kwargs={'pk': self.anuncio1.id})
        response = self.client.get(url)

        # Testa se a resposta tem status code 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Testa se a resposta contém os dados corretos
        self.assertEqual(response.data['id'], self.anuncio1.id)
        
    '''
        Teste que verifica se está funcionando a busca pelos anúncios que retorna a lista
    '''
    def test_get_list_anuncios(self):

        # Faz uma requisição GET para o endpoint
        url = reverse('anuncio-list')
        response = self.client.get(url)

        # Testa se a resposta tem status code 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Testa se dois anúncios são retornados
        self.assertEqual(len(response.data), 2) 

        # Verifica se os ids dos anúncios na resposta correspondem aos anúncios criados
        response_ids = [anuncio['id'] for anuncio in response.data]
        self.assertListEqual(response_ids, [self.anuncio1.id, self.anuncio2.id])
        
    '''
        Teste que verifica se está funcionando a criação de um anúncio
    '''
    def test_create_anuncio(self):
        
        # Parâmetros fictícios
        data = {
            'imovel_id': self.imovel.id,
            'plataforma_id': self.plataforma_anuncio2.id
        }
        
        # Faz uma requisição POST para o endpoint
        url = reverse('anuncio-list')
        response = self.client.post(url, data, format='json')
        
        # Verifica se a resposta tem status code 201 (created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verifica se um anúncio foi de fato criado
        self.assertEqual(Anuncio.objects.count(), 3)
        
        # Verifica se o anúncio criado tem os detalhes corretos
        anuncio = Anuncio.objects.latest('id')
        self.assertEqual(anuncio.imovel, self.imovel)
        self.assertEqual(anuncio.plataforma, self.plataforma_anuncio2)
        
    '''
        Teste que verifica se está funcionando o update de campos de um anúncio (PATCH pois é alteração parcial dos dados)
    '''
    def test_update_anuncio(self):
        
        # Parâmetros fictícios
        new_data = {
            'plataforma_id': self.plataforma_anuncio2.id
        }
        
        # Faz uma requisição PATCH para o endpoint
        url = reverse('anuncio-detail', kwargs={'pk': self.anuncio1.id})
        response = self.client.patch(url, new_data)
        
        # Verifica se a resposta tem status code 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Recarrega o anuncio1 com os dados atualizados do banco
        self.anuncio1.refresh_from_db()
        
        # Verifica se os dados do anúncio foram atualizados corretamente
        self.assertEqual(self.anuncio1.plataforma.id, new_data['plataforma_id'])
        
    '''
        Teste que verifica se o delete realmente está bloqueado
    '''
    def test_delete_anuncio(self):
        
        # Faz uma requisição DELETE para o endpoint
        url = reverse('anuncio-detail', kwargs={'pk': self.anuncio1.id})
        response = self.client.delete(url)
        
        # Verifica se a resposta tem status code 405 (Not Allowed)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)