from django.test import TestCase

from unittest.mock import patch

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from books.models import Book
from books.serializers import BookSerializer

from accounts.models import User


class BookModelTest(TestCase):

    def test_create_book(self):
        Book.objects.create(
            title="Book 1",
            author="Author A", 
            publish_date="1999-08-27", 
            isbn="7197478179712", 
            price=11.11
            )
        book = Book.objects.get(title="Book 1")
        self.assertEqual(str(book), "Book 1")


class BookListAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/books/"  

        Book.objects.create(title="Book 1", author="Author 1", publish_date="2002-12-01", isbn="9761586697301", price=10.99)
        self.book1 = Book.objects.get(title="Book 1")
        Book.objects.create(title="Book 2", author="Author 2", publish_date="1990-01-31", isbn="7043534952345", price=19.99)
        self.book2 = Book.objects.get(title="Book 2")

    def test_book_list_api(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            "books": BookSerializer([self.book1, self.book2], many=True).data
        }
        self.assertEqual(response.json(), expected_data)

class BookCreateAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/book/create/"
        self.user_data = {
            "email": "test@example.com",
            "password": "securepassword123",
        }
        User.objects.create_user(**self.user_data)
        self.user = User.objects.get(email="test@example.com")
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_book_create_api_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        new_book_data = {
            "title": "New Book",
            "author": "New Author",
            "publish_date": "2002-12-01", 
            "isbn": "9761586697301",
            "price": 15.99,
        }

        response = self.client.post(self.url, data=new_book_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Book.objects.filter(title="New Book").exists())

    def test_book_create_api_unauthenticated(self):
        new_book_data = {
            "title": "New Book",
            "author": "New Author",
            "publish_date": "2002-12-01", 
            "isbn": "9761586697301",
            "price": 15.99,
        }

        response = self.client.post(self.url, data=new_book_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertFalse(Book.objects.filter(title="New Book").exists())

class GetBookByIdAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        Book.objects.create(title="Test Book", author="Test Author", publish_date="2002-12-01", isbn="9761586697301", price=19.99)
        self.book = Book.objects.get(title="Test Book")
        self.url = f"/api/book/{self.book.id}/"

    def test_get_book_by_id_api(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            "id": self.book.id,
            "title": self.book.title,
            "author": self.book.author,
            "publish_date": str(self.book.publish_date),
            "isbn": self.book.isbn,
            "price": str(self.book.price),
        }
        self.assertEqual(response.json(), expected_data)

    def test_get_book_by_id_api_not_found(self):
        response = self.client.get("/path/to/get-book/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UpdateBookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        Book.objects.create(title="Test Book", author="Test Author", publish_date="2002-12-01", isbn="9761586697301", price=19.99)
        self.book = Book.objects.get(title="Test Book")
        self.url = f"/api/book/update/{self.book.id}/"
        self.user_data = {
            "email": "test@example.com",
            "password": "securepassword123",
        }
        User.objects.create_user(**self.user_data)
        self.user = User.objects.get(email="test@example.com")
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_update_book_api_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        updated_book_data = {
            "title": "Updated Book",
            "author": "Updated Author",
            "publish_date": "2012-01-12", 
            "isbn": "8346788734433",
            "price": 25.99,
        }

        response = self.client.put(self.url, data=updated_book_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_book = Book.objects.get(id=self.book.id)
        self.assertEqual(updated_book.title, "Updated Book")
        self.assertEqual(updated_book.author, "Updated Author")
        self.assertEqual(str(updated_book.publish_date), "2012-01-12")
        self.assertEqual(updated_book.isbn, "8346788734433")
        self.assertEqual(float(updated_book.price), 25.99)

    def test_update_book_api_unauthenticated(self):
        updated_book_data = {
            "title": "Update Book",
            "author": "Update Author",
            "publish_date": "2012-01-12", 
            "isbn": "8346788734433",
            "price": 15.99,
        }

        response = self.client.put(self.url, data=updated_book_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        not_updated_book = Book.objects.get(id=self.book.id)
        self.assertEqual(not_updated_book.title, "Test Book")

class DeleteBookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        Book.objects.create(title="Test Book", author="Test Author", publish_date="2002-12-01", isbn="9761586697301", price=19.99)
        self.book = Book.objects.get(title="Test Book")
        self.url = f"/api/book/delete/{self.book.id}/"
        self.user_data = {
            "email": "test@example.com",
            "password": "securepassword123",
        }
        User.objects.create_user(**self.user_data)
        self.user = User.objects.get(email="test@example.com")
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_delete_book_api_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(id=self.book.id)

    def test_delete_book_api_unauthenticated(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertTrue(Book.objects.filter(id=self.book.id).exists())