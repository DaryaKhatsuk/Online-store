from django.urls import path
from .views import shop_view, registration_view, login_view, logout_view, cart_view, error_frame_view, \
    password_reset_view, password_reset_done_view

urlpatterns = [
    path('', shop_view, name='base'),
    path('registration/', registration_view, name='registration'),
    path('account/', login_view, name='account'),
    path('logout/', logout_view, name='logout'),
    path('cart/', cart_view, name='cart'),
    path('error_frame/', error_frame_view, name='error_frame'),
    path('account/password_reset/', password_reset_view, name='password_reset'),
    path('account/password_reset/password_reset_done/', password_reset_done_view, name='password_reset_done')
]
