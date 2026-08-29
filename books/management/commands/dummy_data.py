import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from faker import Faker
from books.models import Author, Book, Category, Favorite, Publisher


CATEGORY_NAMES = [
    "رمان",
    "تاریخی",
    "علمی",
    "شعر",
    "فلسفه",
    "کودک و نوجوان",
    "زندگی‌نامه",
    "علوم اجتماعی",
]

PUBLISHER_NAMES = [
    "نشر چشمه",
    "انتشارات نگاه",
    "نشر نیلوفر",
    "انتشارات ققنوس",
    "نشر آگه",
    "انتشارات هرمس",
    "انتشارات مهر",
    "نشر مرکز",
    "انتشارات سوره",
    "نشر راز",
]


class Command(BaseCommand):
    help = "Creates sample data for books, authors, publishers, and categories."

    def add_arguments(self, parser):
        parser.add_argument("--books", type=int, default=50, help="Number of books to create")
        parser.add_argument("--clear", action="store_true", help="Clear existing data before seeding")

    def handle(self, *args, **options):

        fake = Faker("fa_IR")

        if options["clear"]:
            self.clear_data()

        categories = self.create_categories()
        authors = self.create_authors(fake)
        publishers = self.create_publishers()

        for _ in range(options["books"]):
            Book.objects.create(
                title = fake.sentence(nb_words=4).rstrip("."),
                author = random.choice(authors),
                publisher = random.choice(publishers),
                isbn = self.make_isbn(),
                language = random.choice([code for code, _ in Book.LANGUAGE_CHOICES]),
                price = random.randint(50000, 500000),
                pages = random.randint(50, 1000),
                publish_date = date.today() - timedelta(days=random.randint(30, 8000)),
                category = random.choice(categories),
                description=fake.paragraph(nb_sentences=2),
            )

        self.stdout.write(
            self.style.SUCCESS(f"{options['books']} book created successfully.")
        )

    def clear_data(self):
        Favorite.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        Publisher.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write("Existing data cleared.")

    def create_categories(self):
        items = []
        for name in CATEGORY_NAMES:
            obj, _ = Category.objects.get_or_create(name=name)
            items.append(obj)
        return items

    def create_authors(self, fake):
        items = []
        for _ in range(10):
            name = fake.name()
            obj, _ = Author.objects.get_or_create(name=name, defaults={"bio": fake.paragraph(nb_sentences=2)})
            items.append(obj)
        return items

    def create_publishers(self):
        items = []
        for name in PUBLISHER_NAMES:
            obj, _ = Publisher.objects.get_or_create(name=name, defaults={"address": "تهران"})
            items.append(obj)
        return items

    def make_isbn(self):
        while True:
            number = "978" + str(random.randint(100000000, 999999999))
            if not Book.objects.filter(isbn=number).exists():
                return number
