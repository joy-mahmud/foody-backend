from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json,uuid
from .models import Payment
from django.forms.models import model_to_dict
# Create your views here.
@csrf_exempt
def initiate_payment(request):
    if request.method == 'POST':
        try:
            data  = json.loads(request.body)
            amount =  float(data.get('amount'))
            cus_name = data.get('cus_name')
            cus_email = data.get('cus_email')
            num_of_items = int(data.get('num_of_items'))
            print(amount,cus_name,cus_email,num_of_items)
            
            if not (amount and cus_name and cus_email):
                return JsonResponse({"error":"amount, cus_name, cus_email are required"},status = 400)
            tran_id = uuid.uuid4().hex
            print(tran_id)
            Payment.objects.create(tran_id=tran_id,amount=amount,num_of_items=num_of_items,currency='BDT',status = 'INITIATED')  
            payments = Payment.objects.all().order_by("-created_at")
            data = [model_to_dict(payment) for payment in payments]
            return JsonResponse({"payments": data}, safe=False, status=200)
             
        
        
        except Exception as e:
            return JsonResponse({"erro":str(e)},status = 500) 
    
    return JsonResponse({"error":"Only post method is allowed"})
    