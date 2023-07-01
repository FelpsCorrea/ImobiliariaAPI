from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Imovel
from apps.anuncios.models import Anuncio, PlataformaAnuncio
from apps.reservas.models import Reserva
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken

class ImovelApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Configuração do JWT
        self.user = User.objects.create_user(username='user_teste', password='teste@123')
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))
        
        # Cria 2 imoveis fictícios
        self.imovel1 = Imovel.objects.create(
            limite_hospedes=2,
            aceita_animais=True,
            valor_limpeza=100
        )
        self.imovel2 = Imovel.objects.create(
            limite_hospedes=3,
            aceita_animais=False,
            valor_limpeza=150
        )

    '''
        Teste que verifica se está funcionando a busca por um imóvel por seu id
    '''
    def test_get_single_imovel(self):

        # Faz uma requisição GET para o endpoint
        url = reverse('imovel-detail', kwargs={'pk': self.imovel1.id})
        response = self.client.get(url)

        # Testa se a resposta tem status code 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Testa se a resposta contém os dados corretos
        self.assertEqual(response.data['id'], self.imovel1.id)
        
    '''
        Teste que verifica se está funcionando a busca pelos imóveis que retorna a lista
    '''
    def test_get_list_imoveis(self):

        # Faz uma requisição GET para o endpoint
        url = reverse('imovel-list')
        response = self.client.get(url)

        # Testa se a resposta tem status code 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Testa se dois imóveis são retornados
        self.assertEqual(len(response.data), 2) 

        # Verifica se os ids dos imóveis na resposta correspondem aos imóveis criados
        response_ids = [imovel['id'] for imovel in response.data]
        self.assertListEqual(response_ids, [self.imovel1.id, self.imovel2.id])
        
    '''
        Teste que verifica se está funcionando a criação de imóveis
    '''
    def test_create_imovel(self):
        
        # Parâmetros fictícios
        data = {
            'limite_hospedes': 4,
            'aceita_animais': False,
            'valor_limpeza': 200
        }
        
        # Faz uma requisição POST para o endpoint
        url = reverse('imovel-list')
        response = self.client.post(url, data)
        
        # Verifica se a resposta tem status code 201 (created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verifica se um imóvel foi de fato criado
        self.assertEqual(Imovel.objects.count(), 3)
        
        # Verifica se o imóvel criado tem os detalhes corretos
        imovel = Imovel.objects.latest('id')
        self.assertEqual(imovel.limite_hospedes, data['limite_hospedes'])
        self.assertEqual(imovel.aceita_animais, data['aceita_animais'])
        self.assertEqual(imovel.valor_limpeza, data['valor_limpeza'])
        
    '''
        Teste que verifica se está funcionando o update de campos de um imóvel (PATCH pois é alteração parcial dos dados)
    '''
    def test_update_imovel(self):
        
        # Parâmetros fictícios
        new_data = {
            'limite_hospedes': 5,
            'aceita_animais': True
        }
        
        # Faz uma requisição PATCH para o endpoint
        url = reverse('imovel-detail', kwargs={'pk': self.imovel1.id})
        response = self.client.patch(url, new_data)
        
        # Verifica se a resposta tem status code 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Recarrega o imovel1 com os dados atualizados do banco
        self.imovel1.refresh_from_db()
        
        # Verifica se os dados do imovel1 foram atualizados corretamente
        self.assertEqual(self.imovel1.limite_hospedes, new_data['limite_hospedes'])
        self.assertEqual(self.imovel1.aceita_animais, new_data['aceita_animais'])
        
    '''
        Teste que verifica se está funcionando o delete de um imóvel
    '''
    def test_delete_imovel(self):
          
        # Cria uma plataforma
        plataforma_anuncio = PlataformaAnuncio.objects.create(
            taxa=50,
            nome="Airbnb"
        )
        
        imovel = Imovel.objects.create(
            limite_hospedes=3,
            aceita_animais=False,
            valor_limpeza=150
        )
        
        # Cria um anúncio vinculado ao imovel2
        anuncio = Anuncio.objects.create(
            imovel=imovel,
            plataforma=plataforma_anuncio
        )
        
        # Cria uma reserva vinculada ao anuncio
        reserva = Reserva.objects.create(
            anuncio=anuncio,
            comentario="Reserva Teste",
            valor_total=100,
            data_checkin="2023-07-01",
            data_checkout="2023-07-10"
        )
        
        # Faz uma requisição DELETE para o endpoint
        url = reverse('imovel-detail', kwargs={'pk': imovel.id})
        response = self.client.delete(url)
        
        # Verifica se a resposta tem status code 200 (no content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Recarrega o imovel com os dados atualizados do banco
        imovel.refresh_from_db()
        
        # Recarrega o anuncio vinculado ao imovel
        anuncio.refresh_from_db()
        
        # Recarrega a reserva vinculada ao anuncio
        reserva.refresh_from_db()
        
        # É esperado que ao deletar um imovel, delete todos anúncios e ao deletar cada um desses anúncios, deletar todas reservas dele.
        
        # Verifica se o imovel sofreu um "Soft Delete"
        self.assertEqual(imovel.ativo, False)
        
        # Verifica se agora possui 2 imóveis, considerando que 1 foi "deletado"
        self.assertEqual(Imovel.objects.filter(ativo=True).count(), 2)