from django.contrib import admin

from .models import Plorts, Purchase, Comments, Support


@admin.register(Plorts)
class PlortsAdmin(admin.ModelAdmin):
    list_display = ('idPlort', 'plortName', 'imagePlort', 'description', 'rarity', 'price', 'quantity')
    list_filter = ('plortName', 'rarity', 'price')
    search_fields = ('plortName', 'rarity')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('idPurchase', 'boughtPlort', 'pricePlort', 'boughtQuantity', 'totalPrice', 'deliveryAddress',
                    'dateDelivery', 'currentCustomer')
    list_filter = ('totalPrice', 'deliveryAddress', 'dateDelivery', 'currentCustomer')
    search_fields = ('totalPrice', 'deliveryAddress', 'dateDelivery', 'currentCustomer')


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('idComment', 'idPlort', 'idUser', 'UserText')
    list_filter = ('idPlort', 'idUser')
    search_fields = ('idPlort', 'idUser')


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ('idSupport', 'emailUser', 'UserText')
    list_filter = ('emailUser',)
    search_fields = ('emailUser', 'UserText')
