from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status

from rest_framework import serializers
from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer


# Create your views here ~ for CRUD API requests

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# Create your views here.

def book_list(request):
    books = Book.objects.all()
    context = {'book_list': books}
    print(context)
    return render(request, "books/book_list.html", context)


def book_detail(request, id):
    book = Book.objects.get(id=id)
    context = {'book_detail': book}
    return render(request, "books/book_detail.html", context)


@csrf_exempt
def book_collection(request):
    # GET ~ retrieve all the Book objects from the database
    if request.method == 'GET':
        books = Book.objects.all()
        books_serializer = BookSerializer(books, many=True)
        return JSONResponse(books_serializer.data)

    # POST ~ create a new book based on the JSON data included with the HTTP request
    elif request.method == 'POST':
        book_data = JSONParser().parse(request)
        book_serializer = BookSerializer(data=book_data)
        if book_serializer.is_valid():
            book_serializer.save()
            return JSONResponse(book_serializer.data,
                                status=status.HTTP_201_CREATED)


@csrf_exempt
def book_instance(request, id):
    # Check to see if this Book id exists ... if not 404 ERROR
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    # GET ~ retrieve the Book object requested
    if request.method == 'GET':
        book_serializer = BookSerializer(book)
        return JSONResponse(book_serializer.data)

    # PUT ~ update a book based on the JSON data included with the HTTP request
    elif request.method == 'PUT':
        book_data = JSONParser().parse(request)
        book_serializer = BookSerializer(book, data=book_data)
        if book_serializer.is_valid():
            book_serializer.save()
            return JSONResponse(book_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JSONResponse(book_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    # DELETE ~ delete the Book object specified (row in the database)
    elif request.method == 'DELETE':
        book.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
