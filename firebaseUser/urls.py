from django.urls import path
from . import views

urlpatterns = [
    path('save-user',views.save_user,name='save_user')
]
