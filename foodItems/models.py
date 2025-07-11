from django.db import models
class FoodItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()
    origin = models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    rating = models.FloatField(null=True,blank=True)
    image = models.ImageField(upload_to='food-images/')
