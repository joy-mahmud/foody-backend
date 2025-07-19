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

@csrf_exempt
def update_food_item(request, item_id):
    if request.method == 'POST':
        try:
            food = FoodItem.objects.get(id=item_id)

            # Update text fields
            food.title = request.POST.get('title', food.title)
            food.description = request.POST.get('description', food.description)
            food.price = request.POST.get('price', food.price)
            food.quantity = request.POST.get('quantity', food.quantity)
            food.origin = request.POST.get('origin', food.origin)
            food.category = request.POST.get('category', food.category)

            # Update image only if a new one is provided
            if 'image' in request.FILES:
                food.image = request.FILES['image']

            food.save()
            return JsonResponse({'message': 'Food item updated successfully'},status=200)
        
        except FoodItem.DoesNotExist:
            return JsonResponse({'error': 'Food item not found'}, status=404)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

def get_single_food_item(request,item_id):
    if request.method == "GET":
        try:
            food_obj = FoodItem.objects.get(id=item_id)
            food = model_to_dict(food_obj)
            if food_obj.image:
                food['image']= request.build_absolute_uri(food_obj.image.url)
            else:
                food['image'] = None
            return JsonResponse(food)
        except Exception as e:
            return JsonResponse({'error':str(e)},status=400)
    return JsonResponse({'error': 'Only GET method allowed'}, status=405)

@csrf_exempt
def delete_food_item(request,item_id):
    if request.method =="DELETE":
        try:
            food = FoodItem.objects.get(id = item_id)
            food.delete()
            return JsonResponse({"message":"food item deleted successfully"},status=200)
        except FoodItem.DoesNotExist:
            return JsonResponse({'error': 'Food item not found'}, status=404)
    else:
        return JsonResponse({'error': 'Only DELETE method allowed'}, status=405)
            
def get_popular_foods(request):
   if request.method == 'GET':
        try:
            food_items = FoodItem.objects.filter(rating__gt=4).order_by('-rating')[:6]

            data = []
            for item in food_items:
                item_dict = model_to_dict(item)
                item_dict['image'] = request.build_absolute_uri(item.image.url) if item.image else None
                data.append(item_dict)

            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error':str(e)},status=400)
   return JsonResponse({'error': 'Only GET method allowed'}, status=405) 
def get_food_items_by_category(request):
    if request.method == 'GET':
        try:
            category = request.GET.get('category')
            if category:
                food_items = FoodItem.objects.filter(category__iexact=category)
            else:
                food_items = FoodItem.objects.all()

            data = []
            for item in food_items:
                item_dict = model_to_dict(item)
                if item.image:
                    item_dict['image'] = request.build_absolute_uri(item.image.url)
                data.append(item_dict)

            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error':str(e)},status=400)
    return JsonResponse({'error': 'Only GET method allowed'}, status=405) 