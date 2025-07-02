from django.http import JsonResponse
import json
from .models import FirebaseUser
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def save_user(request):
    if request.method == "POST":
        try:
            data =json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            
            if not name or not email:
                return JsonResponse({'error':"Name and email are required"},status = 400)
            user,created =  FirebaseUser.objects.get_or_create(email=email,defaults={'name':name})
            return JsonResponse({'message':"user saved succefully",'created':created})
        except Exception as e:
            return JsonResponse({'error':str(e)},status = 500)
    return JsonResponse({'error':"only post method is allowed"}, status = 405)
