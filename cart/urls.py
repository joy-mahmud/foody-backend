from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/<str:user_email>/', views.get_cart_items, name='get_cart_items'),
]