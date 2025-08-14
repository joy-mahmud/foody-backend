from django.urls import path
from . import views

urlpatterns = [
    path('save-user',views.save_user,name='save_user'),
    path('check-role',views.check_user_role, name='check_role')
]
