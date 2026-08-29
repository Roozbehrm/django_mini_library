from django.contrib import admin
from .models import Author, Book, Category, Publisher


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name", "address")
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publisher", "isbn", "language", "category", "price", "publish_date")
    list_filter = ("category", "author", "publisher", "language", "publish_date")
    search_fields = ("title", "author__name", "publisher__name", "isbn")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)