from django.urls import path
from . import views
urlpatterns = [
    path('payment-init',views.initiate_payment,name="initiate_payment"),
    path('payment/success',views.ssl_success,name="ssl_success"),
    path('payment/fail',views.ssl_fail,name="ssl_fail"),
    path('payment/cancel',views.ssl_fail,name="ssl_cancel"),
]
