from django.urls import path
from .views import shop_view, card_plort, cart_add, cart_detail, cart_remove, \
    registration_view, login_view, logout_view, \
    error_frame_registration_view, error_frame_view, \
    password_reset_view, password_reset_done_view, \
    delete_account_view, delete_account_done_view

urlpatterns = [
    path('', shop_view, name='base'),
    # path('cart/', cart_view, name='cart'),
    path('card_plort_<int:num>/', card_plort, name='card_plort'),
    path('registration/', registration_view, name='registration'),
    path('registration/error_frame_registration', error_frame_registration_view, name='error_frame_registration'),
    path('account/', login_view, name='account'),
    path('logout/', logout_view, name='logout'),
    path('error_frame/', error_frame_view, name='error_frame'),
    path('account/password_reset/', password_reset_view, name='password_reset'),
    path('account/password_reset/password_reset_done/', password_reset_done_view, name='password_reset_done'),
    path('account/delete_account/', delete_account_view, name='delete_account'),
    path('account/delete_account/delete_account_done/', delete_account_done_view, name='delete_account_done'),
    path('cart/', cart_detail, name='cart_detail'),
    path('add/<product_id>/', cart_add, name='cart_add'),
    path('cart/remove/<product_id>/', cart_remove, name='cart_remove'),
]
