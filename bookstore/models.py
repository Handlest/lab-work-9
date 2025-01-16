from django.db import models

class Shelf(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название стеллажа")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость стелажа")
    location = models.CharField(max_length=100, blank=True, verbose_name="Расположение")

    def __str__(self):
        return self.name

class Book(models.Model):
    author = models.CharField(max_length=255, verbose_name="Автор")
    title = models.CharField(max_length=255, verbose_name="Название")
    publisher = models.CharField(max_length=255, verbose_name="Издательство")
    publication_year = models.PositiveIntegerField(verbose_name="Год выпуска")
    genre = models.CharField(max_length=100, verbose_name="Жанр")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    shelf = models.ForeignKey(Shelf, on_delete=models.SET_NULL, null=True, blank=True, related_name="books", verbose_name="Стеллаж")

    def __str__(self):
        return self.title
