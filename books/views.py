from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, request
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from books.forms import AuthorForm, BookForm, CategoryForm, PublisherForm
from books.models import Book, Favorite
from books.selectors import filter_books, list_authors, list_categories, list_publishers
from books.services import delete_author, delete_category, delete_publisher, toggle_favorite


def _is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"

def book_list(request):
    books, form = filter_books(request.GET)

    paginator = Paginator(books, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(
            Favorite.objects.filter(user=request.user).values_list("book_id", flat=True)
        )

    querystring = request.GET.copy()
    querystring.pop("page", None)

    context = {
        "page_obj": page_obj,
        "form": form,
        "favorite_ids": favorite_ids,
        "querystring": querystring.urlencode(),
        "total_count": books.count(),
    }
    return render(request, "books/book_list.html", context)



def book_add(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'کتاب «{book.title}» با موفقیت اضافه شد.')
            return redirect("books:book_list")
    else:
        form = BookForm()
    context = {
        "form": form,
        "mode": "add",
        "author_form": AuthorForm(),
        "publisher_form": PublisherForm(),
        "category_form": CategoryForm(),
    }
    return render(request, "books/book_form.html", context)



def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'کتاب «{book.title}» ویرایش شد.')
            return redirect("books:book_list")
    else:
        form = BookForm(instance=book)
    context = {
        "form": form,
        "mode": "edit",
        "book": book,
        "author_form": AuthorForm(),
        "publisher_form": PublisherForm(),
        "category_form": CategoryForm(),
    }
    return render(request, "books/book_form.html", context)



def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        title = book.title
        book.delete()
        messages.success(request, f'کتاب «{title}» حذف شد.')
        return redirect("books:book_list")
    return render(request, "books/book_confirm_delete.html", {"book": book})



def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, book=book).exists()
    other_books_by_author = Book.objects.filter(author=book.author).exclude(pk=book.pk)
    return render(
        request,
        "books/book_detail.html",
        {"book": book, "is_favorite": is_favorite, "other_books_by_author": other_books_by_author},
    )



def author_add(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            if _is_ajax(request):
                return JsonResponse({"id": author.pk, "name": str(author)})
            messages.success(request, f'نویسنده «{author.name}» اضافه شد.')
            return redirect("books:book_add")
        if _is_ajax(request):
            return JsonResponse({"errors": form.errors}, status=400)
    else:
        form = AuthorForm()

    return render(request, "books/simple_form.html", {"form": form, "title": "افزودن نویسنده جدید"})



def category_add(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            if _is_ajax(request):
                return JsonResponse({"id": category.pk, "name": str(category)})
            messages.success(request, f'دسته‌بندی «{category.name}» اضافه شد.')
            return redirect("books:book_add")
        if _is_ajax(request):
            return JsonResponse({"errors": form.errors}, status=400)

    else:
        form = CategoryForm()
    return render(request, "books/simple_form.html", {"form": form, "title": "افزودن دسته‌بندی جدید"})



def publisher_add(request):
    if request.method == "POST":
        form = PublisherForm(request.POST)
        if form.is_valid():
            publisher = form.save()
            if _is_ajax(request):
                return JsonResponse({"id": publisher.pk, "name": str(publisher)})
            messages.success(request, f'ناشر «{publisher.name}» اضافه شد.')
            return redirect("books:book_add")
        if _is_ajax(request):
            return JsonResponse({"errors": form.errors}, status=400)
    else:
        form = PublisherForm()
    return render(request, "books/simple_form.html", {"form": form, "title": "افزودن ناشر جدید"})



def book_delete_filtered(request):
    if request.method == "POST":
        books, _ = filter_books(request.GET)
        count = books.count()
        if count > 0:
            books.delete()
            messages.success(request, f"{count} کتاب مطابق فیلتر انتخاب‌شده حذف شد.")
        else:
            messages.info(request, "هیچ کتابی مطابق فیلتر فعلی برای حذف وجود نداشت.")
    return redirect("books:book_list")




@login_required
def favorite_toggle(request, pk):
    book = get_object_or_404(Book, pk=pk)
    added = toggle_favorite(request.user, book)
    if added:
        messages.success(request, f'کتاب «{book.title}» به علاقه‌مندی‌ها اضافه شد.')
    else:
        messages.info(request, f'کتاب «{book.title}» از علاقه‌مندی‌ها حذف شد.')
    next_url = request.POST.get("next") or request.GET.get("next") or reverse("books:book_list")
    return redirect(next_url)



@login_required
def favorite_list(request):
    favorites = (
        Favorite.objects.filter(user=request.user)
        .select_related("book", "book__category")
        .order_by("-created_at")
    )
    return render(request, "books/favorites.html", {"favorites": favorites})


def author_list(request):
    context = {
        "title": "مدیریت نویسندگان",
        "items": list_authors(),
        "add_url_name": "books:author_add",
        "delete_url_name": "books:author_delete",
        "is_protected": True,
        "empty_text": "هنوز نویسنده‌ای ثبت نشده است.",
    }
    return render(request, "books/lookup_list.html", context)


def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        ok, error = delete_author(author)
        if ok:
            messages.success(request, f'نویسنده «{author.name}» حذف شد.')
        else:
            messages.error(request, error)
    return redirect("books:author_list")


def publisher_list(request):
    context = {
        "title": "مدیریت ناشران",
        "items": list_publishers(),
        "add_url_name": "books:publisher_add",
        "delete_url_name": "books:publisher_delete",
        "is_protected": True,
        "empty_text": "هنوز ناشری ثبت نشده است.",
    }
    return render(request, "books/lookup_list.html", context)


def publisher_delete(request, pk):
    publisher = get_object_or_404(Publisher, pk=pk)
    if request.method == "POST":
        ok, error = delete_publisher(publisher)
        if ok:
            messages.success(request, f'ناشر «{publisher.name}» حذف شد.')
        else:
            messages.error(request, error)
    return redirect("books:publisher_list")


def category_list(request):
    context = {
        "title": "مدیریت دسته‌بندی‌ها",
        "items": list_categories(),
        "add_url_name": "books:category_add",
        "delete_url_name": "books:category_delete",
        "is_protected": False,
        "empty_text": "هنوز دسته‌بندی‌ای ثبت نشده است.",
    }
    return render(request, "books/lookup_list.html", context)


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        delete_category(category)
        messages.success(request, f'دسته‌بندی «{category.name}» حذف شد.')
    return redirect("books:category_list")
