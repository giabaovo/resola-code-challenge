import django_filters

from books.models import Book

class BookFilter(django_filters.FilterSet):
    author_contains = django_filters.CharFilter(field_name='author', lookup_expr='icontains')

    month = django_filters.NumberFilter(field_name='publish_date__month')

    year = django_filters.NumberFilter(field_name='publish_date__year')

    day = django_filters.NumberFilter(field_name='publish_date__day')

    start_date = django_filters.DateFilter(field_name='publish_date', lookup_expr="gte")

    end_date = django_filters.DateFilter(field_name='publish_date', lookup_expr="lte")


    class Meta:
        model = Book
        fields = ['author', 'publish_date', 'author_contains', 'month', 'year', 'day', 'start_date', 'end_date']