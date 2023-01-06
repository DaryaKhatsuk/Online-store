from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage, get_connection
from django.views.generic import DeleteView, UpdateView
from .forms import CartForm
from .models import Cart


def cart_view(request):
    try:
        context = {
            'form': CartForm(),
        }
        return render(request, 'cart/cart.html', context)
    except:
        return redirect('error_frame')


def error_frame_view(request):
    context = {

    }
    return render(request, 'errors/error_frame.html', context)
