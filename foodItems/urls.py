from django.urls import path
from . import views
urlpatterns = [
    path('all-foods/',views.get_food_items,name="all-foods"),
    path('add-food/',views.add_food_item,name="add-food")
]
