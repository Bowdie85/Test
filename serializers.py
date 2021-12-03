# Created to serialize the Book instances into JSON
from rest_framework import serializers
from books.models import Book

# Class declaring the attributes that represent the fields to be serialized
class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    rank = serializers.IntegerField(required=True)
    title = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=50)
    year = serializers.IntegerField(required=True)

    # Receives validated_data to create new Book instance
    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    # Receives instance and validated_data with which to update Book instance
    def update(self, instance, validated_data):
        # Update values with validated data
        instance.name = validated_data.get('rank', instance.rank)
        instance.title = validated_data.get('title', instance.title )
        instance.author = validated_data.get('author', instance.author)
        instance.year = validated_data.get('year', instance.year)

        # Save the updates
        instance.save()
        # Returns updated Book instance
        return instance
