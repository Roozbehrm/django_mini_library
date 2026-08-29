from django.db.models.deletion import ProtectedError
from books.models import Favorite


def toggle_favorite(user, book):
    favorite, created = Favorite.objects.get_or_create(user=user, book=book)
    if not created:
        favorite.delete()
        return False
    return True

def delete_author(author):
    if author.books.exists():
        return False, f'نویسنده «{author.name}» به {author.books.count()} کتاب وصل است و قابل حذف نیست.'
    try:
        author.delete()
        return True, None
    except ProtectedError:
        return False, f'نویسنده «{author.name}» به یک یا چند کتاب وصل است و قابل حذف نیست.'


def delete_publisher(publisher):
    if publisher.books.exists():
        return False, f'ناشر «{publisher.name}» به {publisher.books.count()} کتاب وصل است و قابل حذف نیست.'
    try:
        publisher.delete()
        return True, None
    except ProtectedError:
        return False, f'ناشر «{publisher.name}» به یک یا چند کتاب وصل است و قابل حذف نیست.'


def delete_category(category):
    category.delete()
    return True, None