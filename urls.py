from django.urls import path
from .views import book_list, book_detail, book_collection, book_instance

urlpatterns = [
    path('api/', book_collection),
    path('api/<id>/', book_instance),
    path('', book_list),
    path('<id>/', book_detail),
]
