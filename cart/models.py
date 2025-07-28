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
