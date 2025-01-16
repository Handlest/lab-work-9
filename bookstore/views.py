from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404



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
        shelf = get_object_or_404(Shelf, id=shelf_id)

        try:
            if not shelf.is_full() and int(shelf.current_occupation) + int(quantity) < int(shelf.capacity):
                Book.objects.create(
                    title=title, author=author, publisher=publisher,
                    genre=genre, publication_year=publication_year, shelf=shelf, quantity=quantity
                )
                shelf.add_books(int(quantity))
                return redirect('book_list')
            else:
                raise ValueError("Невозможно добавить книгу: стеллаж заполнен или не хватает места.")
        except ValueError as e:
            messages.error(request, str(e))  # Показать ошибку пользователю
            # Возвращаем данные обратно в форму
            shelves = Shelf.objects.all()
            return render(request, 'bookstore/add_book.html', {
                    'shelves': shelves,
                    'title': title,
                    'author': author,
                    'publisher': publisher,
                    'publication_year': publication_year,
                    'genre': genre,
                    'quantity': quantity,
                    'shelf_id': shelf_id,
            })
    shelves = Shelf.objects.all()
    return render(request, 'bookstore/add_book.html', {'shelves': shelves})


def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.shelf.add_books(-int(book.quantity))
    book.delete()
    return redirect('book_list')  # Перенаправление на список книг


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
        book.shelf.add_books(int(book.quantity))
        return redirect('book_list')  # Перенаправление на список книг

    return render(request, 'bookstore/edit_book.html', {'book': book, 'shelves': shelves})


def manage_shelves(request):
    shelves = Shelf.objects.all()  # Получаем все стеллажи
    return render(request, 'bookstore/manage_shelves.html', {'shelves': shelves})


def edit_shelf(request, shelf_id):
    shelf = get_object_or_404(Shelf, id=shelf_id)

    if request.method == 'POST':
        # Обрабатываем редактирование вместимости
        new_capacity = request.POST.get('capacity')
        if new_capacity:
            shelf.capacity = int(new_capacity)
            shelf.save()
            return redirect('manage_shelves')

    return render(request, 'bookstore/edit_shelf.html', {'shelf': shelf})
