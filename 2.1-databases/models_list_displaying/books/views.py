from django.shortcuts import render, redirect
from books.models import Book
from django.core.paginator import Paginator


def index_view(request):
    return redirect('books')


def books_view(request):

    books = Book.objects.all()

    template = 'books/books_list.html'
    context = {
        'books': books
    }
    return render(request, template, context)


def pub_date_view(request, pub_date):
    books = Book.objects.filter(pub_date=pub_date)

    prev_date = Book.objects.filter(pub_date__lt=pub_date).order_by('-pub_date').first()
    next_date = Book.objects.filter(pub_date__gt=pub_date).order_by('pub_date').first()

    template = 'books/books_list.html'
    context = {
        'books': books,
        'prev_date': prev_date.pub_date if prev_date else None,
        'next_date': next_date.pub_date if next_date else None,
    }
    return render(request, template, context)
