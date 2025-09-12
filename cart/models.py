from django.db import models
from firebaseUser.models import FirebaseUser
from foodItems.models import FoodItem
class CartItem(models.Model):
    user=models.ForeignKey(FirebaseUser, on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.food.title}"
    
class Order (models.Model):
    user = models.ForeignKey(FirebaseUser,on_delete=models.CASCADE,related_name='orders')
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=20,default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    food_item = models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2)
