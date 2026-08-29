from django.db import models
from django.conf import settings




class Author(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="نام نویسنده")
    bio = models.TextField(blank=True, verbose_name="بیوگرافی")

    class Meta:
        verbose_name = "نویسنده"
        verbose_name_plural = "نویسندگان"
        ordering = ["name"]

    def __str__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته‌بندی")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ["name"]

    def __str__(self):
        return self.name

    

class Publisher(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="نام ناشر")
    address = models.CharField(max_length=255, blank=True, verbose_name="آدرس")

    class Meta:
        verbose_name = "ناشر"
        verbose_name_plural = "ناشران"
        ordering = ["name"]

    def __str__(self):
        return self.name



class Book(models.Model):
    LANGUAGE_CHOICES = [
        ("fa", "فارسی"),
        ("en", "انگلیسی"),
        ("ar", "عربی"),
        ("fr", "فرانسوی"),
        ("de", "آلمانی"),
        ("other", "سایر"),
    ]

    title = models.CharField(max_length=255, verbose_name="عنوان")
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="books", verbose_name="نویسنده")
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT, related_name="books", verbose_name="ناشر")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, verbose_name="زبان")
    price = models.PositiveIntegerField(verbose_name="قیمت (تومان)")
    pages = models.PositiveSmallIntegerField(verbose_name="تعداد صفحات")
    isbn = models.CharField(max_length=20, blank=True, unique=True, verbose_name="شابک (ISBN)",)
    publish_date = models.DateField(verbose_name="تاریخ انتشار")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="books", verbose_name="دسته‌بندی")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "کتاب"
        verbose_name_plural = "کتاب‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.author.name}"

    

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "book")
        verbose_name = "علاقه‌مندی"
        verbose_name_plural = "علاقه‌مندی‌ها"

    def __str__(self):
        return f"{self.user.username} liked {self.book.title}"

