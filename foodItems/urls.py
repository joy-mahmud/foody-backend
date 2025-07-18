from django.urls import path
from . import views
urlpatterns = [
    path('all-foods/',views.get_food_items,name="all-foods"),
    path('add-food/',views.add_food_item,name="add-food"),
    path('update-food/<int:item_id>',views.update_food_item,name="update-food"),
    path('food/<int:item_id>',views.get_single_food_item,name="get_single_food")
]
