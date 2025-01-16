from django.shortcuts import render

from . import models

def book_list(request):
    # Получение параметра поиска из GET-запроса
    query = request.GET.get('query', '').strip()
    books = Book.objects.all()

    # Если есть поисковый запрос, фильтруем книги
    if query:
        books = books.filter(
            models.Q(title__icontains=query) |
            models.Q(author__icontains=query) |
            models.Q(publisher__icontains=query) |
            models.Q(genre__icontains=query)
        )

    return render(request, 'bookstore/book_list.html', {'books': books, 'query': query})

def add_shelf(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')

        # Создать стеллаж
        Shelf.objects.create(name=name, capacity=capacity)
        return redirect('book_list')  # Перенаправление на список книг

    return render(request, 'bookstore/add_shelf.html')


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book, Shelf

def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        publication_year = request.POST.get('publication_year')
        genre = request.POST.get('genre')
        quantity = request.POST.get('quantity')
        shelf_id = request.POST.get('shelf')

        # Найти указанный стеллаж
        shelf = Shelf.objects.get(id=shelf_id) if shelf_id else None

        # Создать книгу
        book = Book.objects.create(
            title=title,
            author=author,
            publisher=publisher,
            publication_year=publication_year,
            genre=genre,
            quantity=quantity,
            shelf=shelf
        )
        return redirect('book_list')  # Перенаправление на список книг

    # Отобразить доступные стеллажи для выбора
    shelves = Shelf.objects.all()
    return render(request, 'bookstore/add_book.html', {'shelves': shelves})
