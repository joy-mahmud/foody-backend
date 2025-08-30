from django.urls import path
from . import views

urlpatterns = [
    path('save-user',views.save_user,name='save_user'),
    path('check-role',views.check_user_role, name='check_role'),
    path('all-users',views.get_all_users,name='all-users'),
    path('delete-user',views.delete_user,name="delete-user")
]
