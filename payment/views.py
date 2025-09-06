from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json,uuid,requests
from .models import Payment
from django.forms.models import model_to_dict
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect

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

            tran_id = uuid.uuid4().hex
            Payment.objects.create(tran_id=tran_id,amount=amount,num_of_items=num_of_items,currency='BDT',status = 'INITIATED')  
            post_data ={
                "store_id" : settings.SSLCZ_STORE_ID,
                "store_passwd" : settings.SSLCZ_STORE_PASS,
                "total_amount" :amount ,
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

def ssl_success(request):
    return redirect(f"http://localhost:5173/payment/success")

def ssl_fail(request):
    return redirect(f"http://localhost:5173/payment/fail")

def ssl_cancel(request):
    return redirect(f"http://localhost:5173/payment/cancel")
    