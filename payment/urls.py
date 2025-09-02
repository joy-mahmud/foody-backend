from django.urls import path
from . import views
urlpatterns = [
    path('payment-init',views.initiate_payment,name="initiate_payment"),
]
