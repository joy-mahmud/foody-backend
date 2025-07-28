from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import CartItem
from foodItems.models import FoodItem
from firebaseUser.models import FirebaseUser

@csrf_exempt
def add_to_cart(request):
    if(request.method == "POST"):
        data=json.loads(request.body)
        food_id = data.get('food_id')
        user_email = data.get('user_email')
        quantity = data.get('quntity',1)
        
        try:
            user = FirebaseUser.objects.get(email=user_email)
            food = FoodItem.objects.get(id=food_id)
            
            cart_item,created = CartItem.objects.get_or_create(user=user,food=food,defaults={'quantity':quantity})
            
            if not created:
                cart_item.quantity+=quantity
                cart_item.save()
                
            return JsonResponse({"message":"Item added to cart succussfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error":str(e)},status=400)
    JsonResponse({"error":"Method not allowed"}, status = 405)

