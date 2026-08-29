from django.db.models import Q , Count
from books.forms import BookFilterForm
from books.models import Book, Author, Publisher, Category


def filter_books(query_params):

    books = Book.objects.select_related("category", "author", "publisher").all()
    form = BookFilterForm(query_params or None)

    if form.is_valid():
        q = form.cleaned_data.get("q")
        author = form.cleaned_data.get("author")
        publisher = form.cleaned_data.get("publisher")
        category = form.cleaned_data.get("category")
        language = form.cleaned_data.get("language")
        min_price = form.cleaned_data.get("min_price")
        max_price = form.cleaned_data.get("max_price")
        date_from = form.cleaned_data.get("date_from")
        date_to = form.cleaned_data.get("date_to")
        sort = form.cleaned_data.get("sort") or "-created_at"

        if q:
            books = books.filter(Q(title__icontains=q) | Q(author__name__icontains=q))
        if author:
            books = books.filter(author=author)
        if publisher:
            books = books.filter(publisher=publisher)
        if category:
            books = books.filter(category=category)
        if language:
            books = books.filter(language=language)
        if min_price is not None:
            books = books.filter(price__gte=min_price)
        if max_price is not None:
            books = books.filter(price__lte=max_price)
        if date_from:
            books = books.filter(publish_date__gte=date_from)
        if date_to:
            books = books.filter(publish_date__lte=date_to)

        books = books.order_by(sort)

    return books, form


def list_authors():
    return Author.objects.annotate(book_count=Count("books")).order_by("name")


def list_publishers():
    return Publisher.objects.annotate(book_count=Count("books")).order_by("name")


def list_categories():
    return Category.objects.annotate(book_count=Count("books")).order_by("name")