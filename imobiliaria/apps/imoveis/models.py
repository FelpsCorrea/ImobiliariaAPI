from django.db import models
from abstracts.models import SoftDeletionModel

class Imovel(SoftDeletionModel):
    id = models.AutoField(primary_key=True)
    data_criacao = models.DateField(auto_now_add=True, editable=False, verbose_name="Data de criacao automatica")
    data_hora_atualizacao = models.DateTimeField(auto_now=True, editable=False, verbose_name="Data atualizada sempre que o objeto da classe é atualizado com .save")
    limite_hospedes = models.IntegerField(null=False)
    quant_banheiros = models.IntegerField(default=0)
    aceita_animais = models.BooleanField(default=False, verbose_name="True se o imóvel aceita animais domesticos")
    valor_limpeza = models.FloatField(default=0)
    data_ativacao = models.DateField(null=True)
    
    class Meta:
        db_table = 'imovel'