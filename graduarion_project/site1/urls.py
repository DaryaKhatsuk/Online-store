from django.urls import path
from .views import shop_view, registration_view, login_view, logout_view, cart_view

urlpatterns = [
    path('', shop_view, name='base'),
    path('registration/', registration_view, name='registration'),
    path('account/', login_view, name='account'),
    path('logout/', logout_view, name='logout'),
    path('cart/', cart_view, name='cart'),
]
