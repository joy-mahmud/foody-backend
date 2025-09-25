from foodItems.models import FoodItem
from firebaseUser.models import FirebaseUser
from cart.models import CartItem,Order
from django.db.models import Avg, Sum
from django.http import JsonResponse

def stats_summary(request):
    if request.method == "GET":
        try:
            total_revenue = Order.objects.aggregate(total=Sum("total_amount"))["total"] or 0
            food_count = FoodItem.objects.count()
            avg_rating = FoodItem.objects.aggregate(avg=Avg("rating"))["avg"] or 0
            user_count = FirebaseUser.objects.count()
            total_orders = Order.objects.count()

            return JsonResponse({
                "total_revenue":total_revenue,
                "food_count": food_count,
                "avg_rating": round(float(avg_rating),2),
                "user_count": user_count,
                "total_orders": total_orders
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)

        
 