from django.http import JsonResponse
from .models import FoodItem 
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def get_food_items(request):
    food_items = FoodItem.objects.all()
    data = [model_to_dict(item)  for item in food_items]
    return JsonResponse(data, safe=False)
    
@csrf_exempt
def add_food_item(request):
    if request.method =="POST":
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            price = request.POST.get('price')
            quantity = request.POST.get('quantity')
            origin = request.POST.get('origin')
            category = request.POST.get('category')
            image = request.FILES.get('image')

            food = FoodItem.objects.create(
                title=title,
                description = description,
                price= price,
                quantity = quantity,
                origin = origin,
                category = category,
                image = image
                )
            return JsonResponse({
                'message':"food item added successfully"
            })
        except Exception as e:
            return JsonResponse({'error':str(e)},status = 500)
        
    return JsonResponse({
        'error':"invalid request method"
    },status = 405)
            
    