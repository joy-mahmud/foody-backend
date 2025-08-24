from foodItems.models import FoodItem
from firebaseUser.models import FirebaseUser
from cart.models import CartItem
from django.db.models import Avg, Sum
from django.http import JsonResponse

def stats_summary(request):
    if request.method == "GET":
        try:
            food_count = FoodItem.objects.count()
            avg_rating = FoodItem.objects.aggregate(avg=Avg("rating"))["avg"] or 0
            avg_price = FoodItem.objects.aggregate(avg=Avg("price"))["avg"] or 0
            user_count = FirebaseUser.objects.count()
            total_cart_qty = CartItem.objects.aggregate(total=Sum("quantity"))["total"] or 0

            return JsonResponse({
                "food_count": food_count,
                "avg_rating": round(float(avg_rating),2),
                "avg_price": round(float(avg_price),2),
                "user_count": user_count,
                "total_cart_qty": total_cart_qty
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)

        
 