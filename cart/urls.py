from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart/',views.add_to_cart,name="add_to_cart"),
    path('cart/<str:user_email>/',views.get_cart_items,name="get_cart_items"),
    path('remove-cart-item/',views.remove_cart_item, name="remove_cart_item"),
    path('update-cart-item-quantity/',views.update_cart_quantity,name="update_cart_item_quantity"),
    path('all-orders',views.get_all_orders,name='get_all_orders')
]
