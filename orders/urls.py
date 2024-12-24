from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.send_order_to_telegram, name='place_order'),
]
