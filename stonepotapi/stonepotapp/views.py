from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import re
import string
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import pymongo


client = pymongo.MongoClient('mongodb://stonepotapi-db-1:27017')

# Access the database
db = client['mealgenie']

# Access the collection
collection = db['dishes']



@api_view(['POST'])
def find_dishes(request):
    search_term = request.data.get('search_term', '')

    if not search_term:
        return JsonResponse({"error": "Missing search term"})

    # Preprocess search term
    processed_search_term = search_term.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_').strip().lower()

    # Search for dishes containing the search term in the ingredients array
    dishes = collection.find({"Ingredients": {"$regex": f".*{processed_search_term}.*", "$options": "i"}})
    results = []
    for dish in dishes:
        result = {
            "DishName": dish["DishName"],
            "Cuisine": dish.get("Cuisine", ""),
            "Course": dish.get("Course", ""),
            "Diet": dish.get("Diet", ""),
            "PrepTimeInMins": dish.get("PrepTimeInMins", ""),
            "Ingredients": dish.get("Ingredients", [])
        }
        results.append(result)

    return JsonResponse({"dishes": results})

@api_view(['GET'])
def get_unique_cuisines(request):
    cuisines = collection.distinct("Cuisine")
    return JsonResponse(cuisines, safe=False)




