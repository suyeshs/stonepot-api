from django.urls import path
from . import views


urlpatterns = [
    path('api/dishes/', views.find_dishes, name='find_dishes'),
    path('api/cuisines/', views.get_unique_cuisines, name='get_unique_cuisines'),
]