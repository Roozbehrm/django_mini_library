from django import forms
from books.models import Author, Book, Category, Publisher



class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "publisher",
            "isbn",
            "language",
            "price",
            "pages",
            "publish_date",
            "category",
            "description",
        ]

        labels = {
            "title": "عنوان کتاب",
            "author": "نویسنده",
            "publisher": "ناشر",
            "isbn": "شابک (ISBN)",
            "language": "زبان",
            "price": "قیمت (تومان)",
            "pages": "تعداد صفحات",
            "publish_date": "تاریخ انتشار",
            "category": "دسته‌بندی",
            "description": "توضیحات",
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "bio"]
        labels = {"name": "نام نویسنده", "bio": "بیوگرافی"}


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ["name", "address"]
        labels = {"name": "نام ناشر", "address": "آدرس"}

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        labels = {"name": "نام دسته‌بندی"}

class BookFilterForm(forms.Form):


    SORT_CHOICES = [
        ("-created_at", "جدیدترین ثبت‌شده"),
        ("-publish_date", "جدیدترین تاریخ انتشار"),
        ("publish_date", "قدیمی‌ترین تاریخ انتشار"),
        ("price", "ارزان‌ترین"),
        ("-price", "گران‌ترین"),
        ("title", "عنوان (الفبا)"),
    ]

    q = forms.CharField(
        required=False,
        label="جستجو (عنوان یا نویسنده)",
    )
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        required=False,
        label="نویسنده",
        empty_label="همه نویسندگان",
    )
    publisher = forms.ModelChoiceField(
        queryset=Publisher.objects.all(),
        required=False,
        label="ناشر",
        empty_label="همه ناشران",
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="دسته‌بندی",
        empty_label="همه دسته‌بندی‌ها",
    )
    language = forms.ChoiceField(
        choices=[("", "همه زبان‌ها")] + list(Book.LANGUAGE_CHOICES),
        required=False,
        label="زبان",
    )
    min_price = forms.IntegerField(
        required=False,
        label="حداقل قیمت",
    )
    max_price = forms.IntegerField(
        required=False,
        label="حداکثر قیمت",
    )
    date_from = forms.DateField(
        required=False,
        label="از تاریخ",
    )
    date_to = forms.DateField(
        required=False,
        label="تا تاریخ",
    )
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        label="مرتب‌سازی",
    )