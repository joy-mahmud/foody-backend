from django.http import JsonResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json,uuid,requests
from .models import Payment
from django.forms.models import model_to_dict
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from firebaseUser.models import FirebaseUser
from cart.models import CartItem,Order,OrderItem

# Create your views here.
def _abs(request,name):
    return request.build_absolute_uri(reverse(name))

@csrf_exempt
def initiate_payment(request):
    if request.method == 'POST':
        try:
            data  = json.loads(request.body)
            amount =  float(data.get('amount'))
            cus_name = data.get('cus_name')
            cus_email = data.get('cus_email')
            num_of_items = int(data.get('num_of_items'))
            
            if not (amount and cus_name and cus_email):
                return JsonResponse({"error":"amount, cus_name, cus_email are required"},status = 400)
            
            try:
                user = FirebaseUser.objects.get(email = cus_email)
            except FirebaseUser.DoesNotExist:
                return JsonResponse({"error":"Invalid user"},status = 404)
            
            cart_items = CartItem.objects.filter(user=user)
            if not cart_items.exists():
                return JsonResponse({"error":"Cart is empty"})
            
            total_amount = 0
            order = Order.objects.create(user=user,total_amount = 0)
            
            for item in cart_items:
                food  = item.food
                quantity = item.quantity
                price = food.price
                subtotal = price*quantity
                total_amount+=subtotal
                
                OrderItem.objects.create(
                    order = order,
                    food_item = food,
                    quantity=quantity,
                    price = price,
                    subtotal = subtotal 
                )
            order.total_amount = total_amount
            order.save()
                 
            tran_id = uuid.uuid4().hex
            Payment.objects.create(order =order, tran_id=tran_id,amount=total_amount,num_of_items=num_of_items,currency='BDT',status = 'INITIATED')  
            post_data ={
                "store_id" : settings.SSLCZ_STORE_ID,
                "store_passwd" : settings.SSLCZ_STORE_PASS,
                "total_amount" :total_amount ,
                "currency" : "BDT",
                "tran_id":tran_id,
                "success_url":_abs(request,"ssl_success"),
                "fail_url":_abs(request,"ssl_fail"),
                "cancel_url":_abs(request,"ssl_cancel"),
                "emi_option":0,
                "cus_name":cus_name,
                "cus_email":cus_email,
                "cus_add1":"Dhaka",
                "cus_city":"Dhaka",
                "cus_postcode":"1200",
                "cus_country":"Bangladesh",
                "cus_phone":"01912564534",
                "shipping_method":"NO",
                "num_of_item":num_of_items,
                "product_profile":"general",
                "product_category":"food",
                "product_name":"Foody order",    
            }
            r = requests.post(settings.SSLCZ_INIT_URL,data = post_data, timeout = 25)
            data = r.json()
            if data.get("status") == "SUCCESS" and data.get("GatewayPageURL"):
                return JsonResponse({'gateway_url': data["GatewayPageURL"],"tran_id":tran_id})
            else:
                return JsonResponse({"error":"unexpected error", "details":data},status = 400)
        
        
        except Exception as e:
            return JsonResponse({"erro":str(e)},status = 500) 
    
    return JsonResponse({"error":"Only post method is allowed"})

def _validate_with_ssl(val_id):
    params ={
        "val_id":val_id,
        "store_id" : settings.SSLCZ_STORE_ID,
        "store_passwd" : settings.SSLCZ_STORE_PASS,
        "format":"json"
    }
    resp = requests.get(settings.SSLCZ_VALIDATION_URL,params=params,timeout=25)
    print("validation response:=>>",resp.json())
    return resp.json()

@csrf_exempt
def ssl_success(request):
    data = request.POST or request.GET 
    val_id = data.get('val_id')
    tran_id = data.get('tran_id')
    if not val_id or not tran_id :
        return HttpResponseBadRequest("Missing val_id/tran_id")
    vres = _validate_with_ssl(val_id)
    status = vres.get("status")
    amount = vres.get("amount")
    if status in ("VALID","VALIDATED"):
        Payment.objects.filter(tran_id=tran_id).update(
            status="PAID",val_id=val_id,gateway_response=vres
        )
        payment  = Payment.objects.get(tran_id=tran_id)
        order = payment.order
        order.status = "CONFIRMED"
        order.save()
        
        #clear the cart 
        CartItem.objects.filter(user=order.user).delete()
        
        return redirect(f"http://localhost:5173/payment/success?tran_id={tran_id}&amount={amount}")
    else:
        Payment.objects.filter(tran_id=tran_id).update(
             status="FAILED",val_id=val_id,gateway_response=vres
        )
        return redirect(f"http://localhost:5173/payment/fail")
    
@csrf_exempt
def ssl_fail(request):
    tran_id = (request.POST or request.GET).get('tran_id')
    if tran_id:
        Payment.objects.filter(tran_id=tran_id).update(status = 'FAILED') 
    return redirect(f"http://localhost:5173/payment/fail")

@csrf_exempt
def ssl_cancel(request):
    tran_id = (request.POST or request.GET).get('tran_id')
    if tran_id:
        Payment.objects.filter(tran_id=tran_id).update(status = 'CANCELLED') 
    return redirect(f"http://localhost:5173/payment/cancel")
    