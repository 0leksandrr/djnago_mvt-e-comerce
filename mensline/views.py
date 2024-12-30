from django.db.models import Count
from django.shortcuts import render, redirect
from slider.models import Slider
from store.models import Product, ReviewRating


def home(request):
    slider_list = Slider.objects.all()

    most_popular_products = Product.objects.all().order_by('created_date')[:12]

    context = {
        'most_popular_products': most_popular_products,
        'slider_list': slider_list
    }
    return render(request, 'home.html', context)
