from rest_framework import serializers

from books.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    def validate(self, attrs):
        if len(attrs.get("isbn")) != 13:
            raise serializers.ValidationError({
                "isbn": "Length of isbn number must be 13 characters"
            }) 
        return attrs