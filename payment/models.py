from django.db import models
from cart.models import Order
class Payment (models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE,related_name='payment',null=True)
    tran_id =models.CharField(max_length=64, unique=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    num_of_items = models.IntegerField(max_length=10)
    currency = models.CharField(max_length=10,default='BDT')
    status = models.CharField(max_length=20,default="INITIATED")
    val_id = models.CharField(max_length=64,blank=True,null=True)
    gateway_response = models.JSONField(default=dict,blank=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
