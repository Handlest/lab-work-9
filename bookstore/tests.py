from django.test import TestCase
from django.urls import reverse
from .models import Book, Shelf


class BookstoreTests(TestCase):
    def setUp(self):
        # Создаем необходимые объекты для тестирования
        self.shelf = Shelf.objects.create(name="Стеллаж 12", capacity=100)
        self.shelf2 = Shelf.objects.create(name="Стеллаж 23", capacity=50)
        self.book1 = Book.objects.create(
            title="Книга 1", author="Автор 1", publisher="Издательство 1",
            genre="Жанр 1", publication_year=2021, quantity=10, shelf=self.shelf
        )
        self.book2 = Book.objects.create(
            title="Книга 2", author="Автор 2", publisher="Издательство 2",
            genre="Жанр 2", publication_year=2022, quantity=5, shelf=self.shelf
        )

    def test_create_book(self):
        """Проверка создания книги"""
        response = self.client.post(reverse('add_book'), {
            'title': 'Новая книга',
            'author': 'Новый автор',
            'publisher': 'Новое издательство',
            'genre': 'Новый жанр',
            'publication_year': 2023,
            'quantity': 3,
            'shelf': self.shelf.id,
        })
        # Проверяем, что книга была добавлена в базу данных
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.status_code, 302)  # Проверка редиректа

    def test_create_shelf(self):
        """Проверка создания стеллажа"""
        response = self.client.post(reverse('add_shelf'), {
            'name': 'Стеллаж 2',
            'capacity': 50,
        })
        # Проверяем, что стеллаж был добавлен в базу данных
        self.assertEqual(Shelf.objects.count(), 3)
        self.assertEqual(response.status_code, 302)  # Проверка редиректа

    def test_book_list_display(self):
        """Проверка отображения списка книг"""
        response = self.client.get(reverse('book_list'))
        # Проверяем, что книги отображаются на странице
        self.assertContains(response, 'Книга 1')
        self.assertContains(response, 'Книга 2')
        self.assertContains(response, 'Автор 1')
        self.assertContains(response, 'Автор 2')

    def test_book_filter_by_author(self):
        """Проверка фильтрации книг по автору"""
        response = self.client.get(reverse('book_list'), {'search': 'Автор 1'})
        # Проверяем, что на странице отображается только одна книга
        self.assertContains(response, 'Книга 1')
        self.assertNotContains(response, 'Книга 2')

    def test_book_filter_by_genre(self):
        """Проверка фильтрации книг по жанру"""
        response = self.client.get(reverse('book_list'), {'search': 'Жанр 2'})
        # Проверяем, что на странице отображается только одна книга
        self.assertContains(response, 'Книга 2')
        self.assertNotContains(response, 'Книга 1')

    # def test_create_book_with_invalid_quantity(self):
    #     """Проверка создания книги с недопустимым количеством"""
    #     response = self.client.post(reverse('add_book'), {
    #         'title': 'Новая книга',
    #         'author': 'Новый автор',
    #         'publisher': 'Новое издательство',
    #         'genre': 'Новый жанр',
    #         'publication_year': 2023,
    #         'quantity': -3,  # Негативный тест с отрицательным количеством
    #         'shelf': self.shelf.id,
    #     })
    #     self.assertEqual(response.status_code, 200)  # Статус код 200, форма не прошла
    #     self.assertContains(response, 'Это поле должно быть больше или равно 1.')  # Проверка на ошибку в поле

    # def test_add_book_to_full_shelf(self):
    #     """Проверка добавления книги на полный стеллаж"""
    #     # Устанавливаем количество книг на стеллаже на максимум
    #     self.shelf.add_books(self.shelf.capacity)
    #
    #     # Пытаемся добавить книгу на полный стеллаж
    #     response = self.client.post(reverse('add_book'), {
    #         'title': 'Книга 3',
    #         'author': 'Автор 3',
    #         'publisher': 'Издательство 3',
    #         'genre': 'Жанр 3',
    #         'publication_year': 2023,
    #         'quantity': 1,
    #         'shelf': self.shelf.id,
    #     })
    #     # Проверяем, что книга не добавилась
    #     self.assertEqual(Book.objects.count(), 2)  # Количество книг не изменилось
    #     self.assertContains(response, 'Стеллаж полный, не может разместить книги.')

    # def test_create_shelf_with_invalid_capacity(self):
    #     """Проверка создания стеллажа с неверной вместимостью"""
    #     response = self.client.post(reverse('add_shelf'), {
    #         'name': 'Стеллаж 3',
    #         'capacity': -10,  # Негативный тест с отрицательной вместимостью
    #     })
    #     self.assertEqual(response.status_code, 200)  # Статус код 200, форма не прошла
    #     self.assertContains(response, 'Вместимость должна быть больше 0.')  # Проверка ошибки в поле вместимости

    def test_book_filter_by_title(self):
        """Проверка фильтрации книг по названию"""
        response = self.client.get(reverse('book_list'), {'search': 'Книга 1'})
        # Проверяем, что на странице отображается только одна книга
        self.assertContains(response, 'Книга 1')
        self.assertNotContains(response, 'Книга 2')

    def test_shelf_capacity_updates_when_adding_books(self):
        """Проверка, что вместимость стеллажа обновляется при добавлении книг"""
        initial_capacity = self.shelf.capacity
        initial_occupation = self.shelf.current_occupation

        # Добавляем 10 книг на стеллаж
        self.client.post(reverse('add_book'), {
            'title': 'Новая книга',
            'author': 'Автор 1',
            'publisher': 'Издательство 1',
            'genre': 'Жанр 1',
            'publication_year': 2023,
            'quantity': 10,
            'shelf': self.shelf.id,
        })

        # Проверяем, что вместимость стеллажа уменьшилась
        self.shelf.refresh_from_db()  # Перезагружаем объект из базы
        self.assertEqual(self.shelf.current_occupation, initial_occupation + 10)
        self.assertEqual(self.shelf.capacity, initial_capacity)

    def test_remove_book_from_shelf(self):
        """Проверка удаления книги из стеллажа"""
        book = Book.objects.create(
            title="Книга для удаления",
            author="Автор 1",
            publisher="Издательство 1",
            genre="Жанр 1",
            publication_year=2023,
            quantity=5,
            shelf=self.shelf
        )

        # Получаем количество книг на стеллаже до удаления
        initial_count = Book.objects.count()

        # Удаляем книгу
        self.client.post(reverse('delete_book', args=[book.id]))

        # Проверяем, что книга была удалена
        self.assertEqual(Book.objects.count(), initial_count - 1)
        self.assertRaises(Book.DoesNotExist, Book.objects.get, id=book.id)