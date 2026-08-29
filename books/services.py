from django.db.models.deletion import ProtectedError
from books.models import Favorite


def toggle_favorite(user, book):

    favorite, created = Favorite.objects.get_or_create(user=user, book=book)
    if not created:
        favorite.delete()
        return False
    return True

