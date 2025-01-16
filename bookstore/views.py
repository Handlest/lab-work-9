from django.db.models import Q

def book_list(request):
    search_query: str = request.GET.get('search', '')  # Получаем поисковый запрос
    # Если запрос непустой, применяем фильтрацию
    if search_query:
        books = Book.objects.filter(
            Q(title__icontains=search_query) |  # Фильтрация по названию
            Q(author__icontains=search_query) |  # Фильтрация по автору
            Q(publisher__icontains=search_query) |  # Фильтрация по издательству
            Q(genre__icontains=search_query)  # Фильтрация по жанру
        )
    else:
        books = Book.objects.all()  # Если запрос пустой, выводим все книги

    return render(request, 'bookstore/book_list.html', {'books': books, 'search_query': search_query})


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


from django.shortcuts import get_object_or_404, redirect
from .models import Book

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('book_list')  # Перенаправление на список книг


from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Shelf

def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    shelves = Shelf.objects.all()

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.publisher = request.POST.get('publisher')
        book.publication_year = request.POST.get('publication_year')
        book.genre = request.POST.get('genre')
        book.quantity = request.POST.get('quantity')
        shelf_id = request.POST.get('shelf')
        book.shelf = Shelf.objects.get(id=shelf_id) if shelf_id else None
        book.save()
        return redirect('book_list')  # Перенаправление на список книг

    return render(request, 'bookstore/edit_book.html', {'book': book, 'shelves': shelves})
