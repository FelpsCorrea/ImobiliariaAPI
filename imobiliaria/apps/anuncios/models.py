from django.db import models
from apps.imoveis.models import Imovel
from abstracts.models import SoftDeletionModel

class PlataformaAnuncio(SoftDeletionModel):
    id = models.AutoField(primary_key=True)
    taxa = models.FloatField(default=0)
    nome = models.CharField(max_length=100, null=False)
    data_criacao = models.DateField(auto_now_add=True, editable=False, verbose_name="Data de criacao automatica")
    data_hora_atualizacao = models.DateTimeField(auto_now=True, editable=False, verbose_name="Data atualizada sempre que o objeto da classe é atualizado com .save")
    
    class Meta:
        db_table = 'plataforma_anuncio'

class Anuncio(SoftDeletionModel):
    id = models.AutoField(primary_key=True)
    data_criacao = models.DateField(auto_now_add=True, editable=False, verbose_name="Data de criacao automatica")
    data_hora_atualizacao = models.DateTimeField(auto_now=True, editable=False, verbose_name="Data atualizada sempre que o objeto da classe é atualizado com .save")
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE, null=False, verbose_name="Imovel que o anuncio pertence")
    plataforma = models.ForeignKey(PlataformaAnuncio, on_delete=models.CASCADE, null=False, verbose_name="Plataforma que o anuncio foi publicado")
    
    class Meta:
        db_table = 'anuncio'