from django.db import models
from apps.anuncios.models import Anuncio
import secrets
import string
from abstracts.models import SoftDeletionModel

'''
    Gera um código aleatório para a reserva e garanta que será único
'''
def generate_random_code():

        while True:
            
            # Gera um código aleatório
            code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(12))
            
            # Verifica se o código já existe
            if Reserva.objects.filter(codigo=code).count() == 0:
                break
        return code

class Reserva(SoftDeletionModel):
    id = models.AutoField(primary_key=True)
    data_hora_criacao = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Data de criacao automatica")
    data_hora_atualizacao = models.DateTimeField(auto_now=True, editable=False, verbose_name="Data atualizada sempre que o objeto da classe é atualizado com .save")
    anuncio = models.ForeignKey(Anuncio, on_delete=models.CASCADE, null=False, verbose_name="Anuncio que a reserva pertence")
    codigo = models.CharField(max_length=12, default=generate_random_code, editable=False, unique=True)
    comentario = models.TextField(blank=True)
    valor_total = models.FloatField(default=0)
    data_checkin = models.DateField(null=False)
    data_checkout = models.DateField(null=False)
    
    class Meta:
        db_table = 'reserva'
    
    