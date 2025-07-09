from django.http import JsonResponse
from .models import FoodItem 
from django.forms.models import model_to_dict
# Create your views here.

def get_food_items(request):
    food_items = FoodItem.objects.all()
    data = [model_to_dict(item)  for item in food_items]
    return JsonResponse(data, safe=False)
    
