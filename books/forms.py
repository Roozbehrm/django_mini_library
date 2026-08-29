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
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "عنوان کتاب"}),
            "author": forms.Select(attrs={"class": "form-select"}),
            "publisher": forms.Select(attrs={"class": "form-select"}),
            "isbn": forms.TextInput(attrs={"class": "form-control", "placeholder": "مثلاً 9786001824970"}),
            "language": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "قیمت به تومان"}),
            "pages": forms.NumberInput(attrs={"class": "form-control", "placeholder": "تعداد صفحه"}),
            "publish_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "توضیحات (اختیاری)"}
            ),
        }
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
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "نام نویسنده جدید"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "بیوگرافی (اختیاری)"}),
        }
        labels = {"name": "نام نویسنده", "bio": "بیوگرافی"}


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ["name", "address"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "نام ناشر جدید"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "آدرس (اختیاری)"}),
        }       
        labels = {"name": "نام ناشر", "address": "آدرس"}

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "form-control", "placeholder": "نام دسته‌بندی جدید"})}        
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
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "نام کتاب یا نویسنده..."}),
    )
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        required=False,
        label="نویسنده",
        empty_label="همه نویسندگان",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    publisher = forms.ModelChoiceField(
        queryset=Publisher.objects.all(),
        required=False,
        label="ناشر",
        empty_label="همه ناشران",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="دسته‌بندی",
        empty_label="همه دسته‌بندی‌ها",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    language = forms.ChoiceField(
        choices=[("", "همه زبان‌ها")] + list(Book.LANGUAGE_CHOICES),
        required=False,
        label="زبان",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    min_price = forms.DecimalField(
        required=False,
        label="حداقل قیمت",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    max_price = forms.DecimalField(
        required=False,
        label="حداکثر قیمت",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    date_from = forms.DateField(
        required=False,
        label="از تاریخ",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    date_to = forms.DateField(
        required=False,
        label="تا تاریخ",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        label="مرتب‌سازی",
        widget=forms.Select(attrs={"class": "form-select"}),
    )