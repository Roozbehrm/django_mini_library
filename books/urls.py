from django.urls import path
from books import views


app_name = "books"

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.book_add, name='book_add'),
    path('edit/<int:pk>/', views.book_edit, name='book_edit'),
    path('delete/<int:pk>/', views.book_delete, name='book_delete'),
    path('detail/<int:pk>/', views.book_detail, name='book_detail'),
    path('author/add/', views.author_add, name='author_add'),
    path('category/add/', views.category_add, name='category_add'),
    path('publisher/add/', views.publisher_add, name='publisher_add'),
    path('delete-filtered/', views.book_delete_filtered, name='book_delete_filtered'),
    path('favorite/toggle/<int:pk>/', views.favorite_toggle, name='favorite_toggle'),
    path('favorites/', views.favorite_list, name='favorite_list'),

]