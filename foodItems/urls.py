from django.urls import path
from . import views
urlpatterns = [
    path('all-foods/',views.get_food_items,name="all-foods")
]
