from django.http import JsonResponse
from .models import FoodItem 
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

# def get_food_items(request):
#     food_items = FoodItem.objects.all()
#     data = [model_to_dict(item)  for item in food_items]
#     return JsonResponse(data, safe=False)
def get_food_items(request):
    food_items = FoodItem.objects.all()
    data = []
    for item in food_items:
        item_dict = model_to_dict(item)
        # Add full image URL manually
        if item.image:
            item_dict['image'] = request.build_absolute_uri(item.image.url)
        else:
            item_dict['image'] = None

        data.append(item_dict)

    return JsonResponse(data, safe=False)

@csrf_exempt
def add_food_item(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            price = request.POST.get('price')
            quantity = request.POST.get('quantity')
            origin = request.POST.get('origin')
            category = request.POST.get('category')
            rating = request.POST.get('rating')
            image = request.FILES.get('image')

            if not title or not image:
                return JsonResponse({'error': 'Title and image are required'}, status=400)

            food = FoodItem.objects.create(
                title=title,
                description=description,
                price=price,
                quantity=quantity,
                origin=origin,
                category=category,
                rating=rating,
                image=image
            )

            return JsonResponse({
                'message': 'Food item uploaded successfully',
                # 'image_url': request.build_absolute_uri(food.image.url)
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
    
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
            
    