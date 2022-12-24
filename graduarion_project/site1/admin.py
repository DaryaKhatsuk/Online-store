from django.contrib import admin
from .models import Plorts


@admin.register(Plorts)
class PlortsAdmin(admin.ModelAdmin):
    list_display = ('idPlort', 'plortName', 'imagePlort', 'description', 'rarity', 'price', 'quantity')
    list_filter = ('plortName', 'rarity', 'price')
    search_fields = ('plortName', 'rarity')
