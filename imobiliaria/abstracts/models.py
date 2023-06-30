from django.db import models

'''
    Classe abstrata para usar do método de Soft Delete
'''
class SoftDeletionModel(models.Model):
    ativo = models.BooleanField(default=True)

    def delete(self):
        self.ativo = False
        self.save()

    class Meta:
        abstract = True