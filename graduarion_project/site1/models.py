from django.db import models


class Comments(models.Model):
    idComment = models.AutoField(primary_key=True, verbose_name='Key')
    idPlort = models.IntegerField(verbose_name='Key Plort')
    idUser = models.IntegerField(verbose_name='Key User')
    userName = models.CharField(max_length=200, verbose_name='User name')
    UserText = models.CharField(max_length=1024, verbose_name='Comment')
    dateOrder = models.DateField(auto_now_add=True)


class Plorts(models.Model):
    idPlort = models.AutoField(primary_key=True, verbose_name='Key')
    plortName = models.CharField(max_length=100, verbose_name='Plort name')
    imagePlort = models.CharField(max_length=200, verbose_name='ImagePlort')
    description = models.CharField(max_length=400, verbose_name='Description')
    rarity = models.CharField(max_length=20, choices=(("R", "Rare"), ("O", "Ordinary")), null=True)
    price = models.IntegerField(verbose_name='Price')
    quantity = models.IntegerField(verbose_name='Quantity')

    def __str__(self):
        return f'{self.plortName}'

    class Meta:
        verbose_name = "Plort"
        verbose_name_plural = "Plorts"
        ordering = ('plortName',)


class Purchase(models.Model):
    idPurchase = models.AutoField(primary_key=True, verbose_name='Key')
    boughtPlort = models.CharField(max_length=100, verbose_name='Plort')
    pricePlort = models.IntegerField(verbose_name='Price')
    boughtQuantity = models.IntegerField(verbose_name='Quantity')
    totalPrice = models.IntegerField(verbose_name='Total price')

    deliveryAddress = models.CharField(max_length=200, verbose_name='Delivery address')
    dateDelivery = models.DateField()
    dateOrder = models.DateField(auto_now_add=True)

    currentCustomer = models.IntegerField(verbose_name='Customer')


class Support(models.Model):
    idSupport = models.AutoField(primary_key=True, verbose_name='Key')
    emailUser = models.CharField(max_length=100, verbose_name='Email')
    UserText = models.CharField(max_length=2000, verbose_name='Message')
