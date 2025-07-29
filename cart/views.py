from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import CartItem
from foodItems.models import FoodItem
from firebaseUser.models import FirebaseUser

# Create your views here.
@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        food_id = data.get('food_id')
        user_email = data.get('user_email')  # or use request.user.id if using authentication
        quantity = data.get('quantity', 1)

        try:
            user = FirebaseUser.objects.get(email=user_email)
            food = FoodItem.objects.get(id=food_id)

            cart_item, created = CartItem.objects.get_or_create(
                user=user,
                food=food,
                defaults={'quantity': quantity}
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return JsonResponse({"message": "Item added to cart successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
def get_cart_items(request, user_email):
    try:
        user = FirebaseUser.objects.get(email=user_email)
        cart_items = CartItem.objects.filter(user=user).select_related('food')
        print(cart_items)
        data = []
        for item in cart_items:
            food = item.food
            data.append({
                "id": item.id,
                "food_id": food.id,
                "title": food.title,
                "description": food.description,
                "price": float(food.price),
                "quantity": item.quantity,
                "image": request.build_absolute_uri(food.image.url) if food.image else None,
                "rating": food.rating,
                "category": food.category,
                "origin": food.origin,
            })

        return JsonResponse(data, safe=False)

    except FirebaseUser.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)