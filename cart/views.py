from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import CartItem,Order,OrderItem
from foodItems.models import FoodItem
from firebaseUser.models import FirebaseUser
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

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
                "quantity":item.quantity,
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

@csrf_exempt
def update_cart_quantity(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)
            cart_item_id = data.get("cart_item_id")
            quantity = data.get("quantity")
            item = CartItem.objects.get(id = cart_item_id)
            item.quantity = quantity
            item.save()
            return JsonResponse({"message":"quantity updated"},status = 200)
        except CartItem.DoesNotExist:
            return JsonResponse({"error":"Item not found"},status = 404)
    else:
        return JsonResponse({"error":"method not allowed"},status = 400)
    
def get_all_orders(request):
    if request.method=='GET':
        try:
            page_number = request.GET.get('page',1)
            page_size = request.GET.get('page_size',5)
            
            try:
                page_size = int(page_size)
                if page_size <=0:
                    raise ValueError
            except ValueError:
                return JsonResponse({"error":"Invalid Page_size"},status = 400)
            
            orders = Order.objects.all().order_by("-created_at")
            paginator = Paginator(orders,page_size)
            
            try:
                page_obj = paginator.page(page_number)
            except PageNotAnInteger:
                return JsonResponse({"error":"Invalid page number"},status = 400)
            except EmptyPage:
                return JsonResponse({"error":"Page out of range"},status = 404)
            
            data  = []
            for order in page_obj.object_list:
                order_dict ={
                    "id":order.id,
                    "user":{
                        "id":order.user.id,
                        "name":order.user.name,
                        "email":order.user.email
                    },
                    "total_amount":order.total_amount,
                    "status":order.status,
                    "created_at":order.created_at,
                    "updated_at":order.updated_at,
                    "items":[]
                }
                
                for item in order.items.all():
                    order_dict["items"].append({
                        "id":item.id,
                        "food_item":{
                            "id":item.food_item.id,
                            "name":item.food_item.title,
                            "price":item.food_item.price,
                            "image":request.build_absolute_uri(item.food_item.image.url) if item.food_item.image else None
                        },
                        "price":item.price,
                        "quantity":item.quantity,
                        "subtotal":item.subtotal
                    })
                data.append(order_dict)
            return JsonResponse ({
                "count":paginator.count,
                "num_of_pages":paginator.num_pages,
                "current_page":page_obj.number,
                "result":data
            })
        except Exception as e:
            return JsonResponse({"error":str(e)},status = 500)
    return JsonResponse({"error":"only get method is allowed"},status = 400)    
        