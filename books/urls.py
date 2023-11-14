from django.urls import path

from books.api import BookListAPI, BookCreateAPI, GetBookByIdAPI, UpdateBook, DeleteBook

urlpatterns = [
    path("books/", BookListAPI.as_view(), name="books-list"),
    path("book/<int:pk>/", GetBookByIdAPI.as_view(), name="book-by-id"),
    path("book/create/", BookCreateAPI.as_view(), name="book-create"),
    path("book/update/<int:pk>/", UpdateBook.as_view(), name="book-update"),
    path("book/delete/<int:pk>/", DeleteBook.as_view(), name="book-delete"),
]
