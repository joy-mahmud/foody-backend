from django.http import JsonResponse
import json
from .models import FirebaseUser
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
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

def get_all_users(request):
    if request.method == "GET":
        try:
            users = FirebaseUser.objects.all()
            data = []
            for user in users:
                user_dict = model_to_dict(user,fields=['id','name','email','role'])
                data.append(user_dict)
            return JsonResponse({"users":data},safe=False,status=200)
        
        except Exception as e:
            return JsonResponse({"error":str(e)},status = 500)
    return JsonResponse({"error":"Invalid request method"},status = 405)

@csrf_exempt
def check_user_role(request):
    if request.method == 'POST':
        try:
            data= json.loads(request.body)
            user_email = data.get('user_email')
            print(user_email)
            if not user_email:
                return JsonResponse({'error':'Email is required'},status = 400)
            try:
                user = FirebaseUser.objects.get(email = user_email)
                return JsonResponse({'role':user.role})
            except FirebaseUser.DoesNotExist:
               return JsonResponse({'error':"user not found"},status = 404)   
        except Exception as e:
           return JsonResponse({'error':str(e)},status = 500)
            
    return JsonResponse({'error':"only post method is allowed"}, status = 405)    
