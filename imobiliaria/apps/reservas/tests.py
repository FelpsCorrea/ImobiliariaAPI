from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from .models import Reserva
from apps.anuncios.models import Anuncio, PlataformaAnuncio
from apps.imoveis.models import Imovel

class ReservaApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Cria um imóvel fictício
        self.imovel = Imovel.objects.create(
            limite_hospedes=2,
            aceita_animais=True,
            valor_limpeza=100,
            data_ativacao=timezone.now().date()
        )
        
        # Cria uma plataforma
        plataforma_anuncio = PlataformaAnuncio.objects.create(
            taxa=50,
            nome="Airbnb"
        )
        
        # Cria um anúncio vinculado ao imovel2
        self.anuncio = Anuncio.objects.create(
            imovel=self.imovel,
            plataforma=plataforma_anuncio
        )
        
        # Cria duas reservas fictícias vinculadas ao anúncio
        self.reserva1 = Reserva.objects.create(
            anuncio=self.anuncio,
            comentario="Reserva Teste1",
            valor_total=100,
            data_checkin="2023-07-01",
            data_checkout="2023-07-02"
        )
        self.reserva2 = Reserva.objects.create(
            anuncio=self.anuncio,
            comentario="Reserva Teste2",
            valor_total=200,
            data_checkin="2023-07-03",
            data_checkout="2023-07-04"
        )

    '''
        Teste que verifica se está funcionando a busca por uma reserva por seu id
    '''
    def test_get_single_reserva(self):

        # Faz uma requisição GET para o endpoint
        url = reverse('reserva-detail', kwargs={'pk': self.reserva1.id})
        response = self.client.get(url)

        # Testa se a resposta tem status code 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Testa se a resposta contém os dados corretos
        self.assertEqual(response.data['id'], self.reserva1.id)
        
    '''
        Teste que verifica se está funcionando a busca pelas reservas que retorna a lista
    '''
    def test_get_list_reservas(self):

        # Faz uma requisição GET para o endpoint
        url = reverse('reserva-list')
        response = self.client.get(url)

        # Testa se a resposta tem status code 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Testa se duas reservas são retornadas
        self.assertEqual(len(response.data), 2)

        # Verifica se os ids das reservas na resposta correspondem as reservas criadas
        response_ids = [reserva['id'] for reserva in response.data]
        self.assertListEqual(response_ids, [self.reserva1.id, self.reserva2.id])
        
    '''
        Teste que verifica se está funcionando a criação de reservas
    '''
    def test_create_reserva(self):
        
        url = reverse('reserva-list')
        
        #------------------------------------------------------------------------------------------------------
        # Parâmetros que devem funcionar
        data = {
            'anuncio_id': self.anuncio.id,
            'comentario': "Reserva Teste3",
            'valor_total': 300,
            'data_checkin': "2023-07-14",
            'data_checkout': "2023-07-15"
        }
        
        # Faz uma requisição POST para o endpoint
        response = self.client.post(url, data)
        
        # Verifica se a resposta tem status code 201 (created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verifica se uma reserva foi de fato criada
        self.assertEqual(Reserva.objects.count(), 3)
        
        # Verifica se a reserva criada tem os detalhes corretos
        reserva = Reserva.objects.latest('id')
        self.assertEqual(reserva.anuncio.id, data['anuncio_id'])
        self.assertEqual(reserva.comentario, data['comentario'])
        self.assertEqual(reserva.valor_total, data['valor_total'])
        self.assertEqual(str(reserva.data_checkin), data['data_checkin'])
        self.assertEqual(str(reserva.data_checkout), data['data_checkout'])
        
        #------------------------------------------------------------------------------------------------------
        # Parâmetros fictícios que devem falhar (Por já existir uma reserva para essa data)
        data_fail1 = {
            'anuncio_id': self.anuncio.id,
            'comentario': "Reserva Teste3",
            'valor_total': 300,
            'data_checkin': "2023-07-03",
            'data_checkout': "2023-07-04"
        }
         
        # Faz uma requisição POST para o endpoint
        response1 = self.client.post(url, data_fail1, format='json')
        
        # Verifica se a resposta tem status code 400 (BAD REQUEST)
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        
        #------------------------------------------------------------------------------------------------------
        # Parâmetros fictícios que devem falhar (Por a data de checkin ser superior à data de checkout)
        data_fail2 = {
            'anuncio_id': self.anuncio.id,
            'comentario': "Reserva Teste3",
            'valor_total': 300,
            'data_checkin': "2023-07-15",
            'data_checkout': "2023-07-14"
        }
        
        # Faz uma requisição POST para o endpoint
        response2 = self.client.post(url, data_fail2)
        
        # Verifica se a resposta tem status code 400 (BAD REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        
        #------------------------------------------------------------------------------------------------------
        # Parâmetros fictícios que devem falhar (Por a data de checkin e checkout serem no passado)
        data_fail3 = {
            'anuncio_id': self.anuncio.id,
            'comentario': "Reserva Teste3",
            'valor_total': 300,
            'data_checkin': "2022-07-15",
            'data_checkout': "2022-07-14"
        }
        # Faz uma requisição POST para o endpoint
        response3 = self.client.post(url, data_fail3)
        
        # Verifica se a resposta tem status code 400 (BAD REQUEST)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        
        #------------------------------------------------------------------------------------------------------
        # Parâmetros fictícios que devem falhar (Por não existir o anúncio informado)
        data_fail4 = {
            'anuncio_id': "10",
            'valor_total': 300,
            'data_checkin': "2023-07-14",
            'data_checkout': "2023-07-15"
        }
        
        # Faz uma requisição POST para o endpoint
        response4 = self.client.post(url, data_fail4)
        
        # Verifica se a resposta tem status code 400 (BAD REQUEST)
        self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)
        
        #------------------------------------------------------------------------------------------------------
        # Parâmetros que devem falhar (Por o comentário estar em branco)
        data_fail5 = {
            'anuncio_id': self.anuncio.id,
            'comentario': "",
            'valor_total': 300,
            'data_checkin': "2023-07-14",
            'data_checkout': "2023-07-15"
        }
        
        # Faz uma requisição POST para o endpoint
        response5 = self.client.post(url, data_fail5)
        
        # Verifica se a resposta tem status code 500 (BAD REQUEST)
        self.assertEqual(response5.status_code, status.HTTP_400_BAD_REQUEST)
        
        #------------------------------------------------------------------------------------------------------
        # Parâmetros que devem falhar (Por o valor total estar negativo)
        data_fail6 = {
            'anuncio_id': self.anuncio.id,
            'comentario': "Reserva Teste",
            'valor_total': -300,
            'data_checkin': "2023-07-14",
            'data_checkout': "2023-07-15",
        }
        
        # Faz uma requisição POST para o endpoint
        response6 = self.client.post(url, data_fail6)
        
        # Verifica se a resposta tem status code 500 (BAD REQUEST)
        self.assertEqual(response6.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    '''
        Teste que verifica se o update realmente está bloqueado
    '''
    def test_update_reserva(self):
        
        new_data = {
            'comentario': "Reserva Teste4"
        }
        
        url = reverse('reserva-detail', kwargs={'pk': self.reserva1.id})
        
        # Faz uma requisição PATCH para o endpoint
        response = self.client.patch(url, new_data)
        
        # Verifica se a resposta tem status code 405 (Not Allowed)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Faz uma requisição POST para o endpoint
        response = self.client.post(url, new_data)
        
        # Verifica se a resposta tem status code 405 (Not Allowed)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    '''
        Teste que verifica se está funcionando o delete de uma reserva
    '''
    def test_delete_reserva(self):
        
        # Faz uma requisição DELETE para o endpoint
        url = reverse('reserva-detail', kwargs={'pk': self.reserva2.id})
        response = self.client.delete(url)
        
        # Verifica se a resposta tem status code 200 (no content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Recarrega o reserva2 com os dados atualizados do banco
        self.reserva2.refresh_from_db()
        
        # Verifica se a reserva2 sofreu um "Soft Delete"
        self.assertEqual(self.reserva2.ativo, False)