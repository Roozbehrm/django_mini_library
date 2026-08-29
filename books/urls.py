from django.urls import path
from books import views


app_name = "books"

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("book/add/", views.book_add, name="book_add"),
    path("book/<int:pk>/", views.book_detail, name="book_detail"),
    path("book/<int:pk>/edit/", views.book_edit, name="book_edit"),
    path("book/<int:pk>/delete/", views.book_delete, name="book_delete"),
    path("books/delete-filtered/", views.book_delete_filtered, name="book_delete_filtered"),
    path("book/<int:pk>/favorite/", views.favorite_toggle, name="favorite_toggle"),
    path("favorites/", views.favorite_list, name="favorite_list"),
    path("authors/add/", views.author_add, name="author_add"),
    path("publishers/add/", views.publisher_add, name="publisher_add"),
    path("categories/add/", views.category_add, name="category_add"),
    path("authors/", views.author_list, name="author_list"),
    path("authors/<int:pk>/delete/", views.author_delete, name="author_delete"),
    path("publishers/", views.publisher_list, name="publisher_list"),
    path("publishers/<int:pk>/delete/", views.publisher_delete, name="publisher_delete"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
]