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
def get_cart_items(request,user_email):
    try:
        user = FirebaseUser.objects.get(email = user_email)
        cart_items = CartItem.objects.filter(user=user).select_related('food')
        print(cart_items)
        data = []
        for item in cart_items:
            food = item.food
            data.append({
                "id":item.id,
                "food_id":food.id,
                "title":food.title,
                "description":food.description,
                "price":food.price,
                "quantity":food.quantity,
                "image":request.build_absolute_uri(food.image.url) if food.image else None,
                "rating":food.rating,
                "category":food.category,
                "origin":food.origin
            })
        return JsonResponse(data,safe=False)
    except FirebaseUser.DoesNotExist:
        return JsonResponse({"error":"User not found"},status = 404)
    
@csrf_exempt   
def remove_cart_item(request):
    if request.method =="DELETE":
        try:
            data = json.loads(request.body)
            cart_item_id = data.get("cart_item_id")
            item = CartItem.objects.get(id=cart_item_id)
            item.delete()
            return JsonResponse({"message":"cart item deleted successfully"},status = 200)
        except CartItem.DoesNotExist:
            return JsonResponse({"error":"item not found"}, status = 404)