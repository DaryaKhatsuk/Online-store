from django.urls import path
from .views import cart_view, error_frame_view

urlpatterns = [
    path('', cart_view, name='cart'),
    path('error_frame/', error_frame_view, name='error_frame'),
]
