from django.db import models


class Plorts(models.Model):
    idPlort = models.AutoField(primary_key=True, verbose_name='Key')
    plortName = models.CharField(max_length=30, verbose_name='Plort name')
    imagePlort = models.CharField(max_length=200, verbose_name='ImagePlort')
    description = models.CharField(max_length=395, verbose_name='Description')
    rarity = models.CharField(max_length=20, choices=(("R", "Rare"), ("O", "Ordinary")))
    price = models.IntegerField(verbose_name='Price')
    quantity = models.IntegerField(verbose_name='Quantity')

    def __str__(self):
        return f'{self.plortName}'

    class Meta:
        verbose_name = "Plort"
        verbose_name_plural = "Plorts"
        ordering = ('plortName',)


class CartModel(models.Model):
    pass
