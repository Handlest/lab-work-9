from django.contrib import admin
from .models import Book, Shelf

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'publication_year', 'genre', 'quantity', 'shelf')
    search_fields = ('title', 'author', 'publisher', 'genre')
    list_filter = ('genre', 'publisher', 'author')
    ordering = ('title',)

@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'current_occupation', 'is_full')
    search_fields = ('name',)
    ordering = ('name',)
