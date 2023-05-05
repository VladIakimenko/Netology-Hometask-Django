from django.contrib import admin
from django.urls import path, register_converter

from books.converters import DateConverter
from books.views import books_view, index_view, pub_date_view

register_converter(DateConverter, 'pub_dt')

urlpatterns = [
    path('', index_view, name='index'),
    path('admin/', admin.site.urls),
    path('books/', books_view, name='books'),
    path('books/<pub_dt:pub_date>/', pub_date_view, name='pub_date'),
]
