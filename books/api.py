from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from books.models import Book

from books.serializers import BookSerializer

class BookListAPI(ListAPIView):
    # API get list of books
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):
        custom_response = {
            "books": BookSerializer(self.get_queryset(), many=True).data
        }
        return Response(custom_response, status=status.HTTP_200_OK)

class BookCreateAPI(CreateAPIView):
    # API create a new book
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class GetBookByIdAPI(RetrieveAPIView):
    # API get book by Id
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class UpdateBook(UpdateAPIView):
    # API update book by Id
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class DeleteBook(DestroyAPIView):
    # API delete book by Id
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]