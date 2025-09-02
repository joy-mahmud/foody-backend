from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
@csrf_exempt
def initiate_payment(request):
    if request.method == 'POST':
        data  = json.loads(request.body)
        print(data)
        return JsonResponse({'message':'payment data received'})
    
    return JsonResponse({"error":"Only post method is allowed"})
    