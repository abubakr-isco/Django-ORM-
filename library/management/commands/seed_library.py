from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand

from library.models import Author, Book

AUTHORS = [
    ("Лев Толстой", "Россия", date(1828, 9, 9)),
    ("Фёдор Достоевский", "Россия", date(1821, 11, 11)),
    ("Антон Чехов", "Россия", date(1860, 1, 29)),
    ("George Orwell", "UK", date(1903, 6, 25)),
    ("J. K. Rowling", "UK", date(1965, 7, 31)),
    ("Stephen King", "USA", date(1947, 9, 21)),
]

BOOKS = [
    ("Война и мир", "Лев Толстой", 1300, "25.00", date(1869, 1, 1)),
    ("Анна Каренина", "Лев Толстой", 864, "19.90", date(1877, 1, 1)),
    ("Воскресение", "Лев Толстой", 512, "12.50", date(1899, 1, 1)),
    ("Преступление и наказание", "Фёдор Достоевский", 672, "15.00", date(1866, 1, 1)),
    ("Идиот", "Фёдор Достоевский", 640, "14.00", date(1869, 1, 1)),
    ("Братья Карамазовы", "Фёдор Достоевский", 824, "18.00", date(1880, 11, 1)),
    ("Бесы", "Фёдор Достоевский", 768, "16.00", date(1872, 1, 1)),
    ("Палата № 6", "Антон Чехов", 96, "5.00", date(1892, 11, 1)),
    ("Вишнёвый сад", "Антон Чехов", 80, "4.50", date(1904, 1, 17)),
    ("Чайка", "Антон Чехов", 72, "4.00", date(1896, 10, 17)),
    ("1984", "George Orwell", 328, "11.99", date(1949, 6, 8)),
    ("Animal Farm", "George Orwell", 112, "8.99", date(1945, 8, 17)),
    ("Homage to Catalonia", "George Orwell", 232, "10.50", date(1938, 4, 25)),
    ("Harry Potter and the Philosopher's Stone", "J. K. Rowling", 223, "9.99", date(1997, 6, 26)),
    ("Harry Potter and the Chamber of Secrets", "J. K. Rowling", 251, "9.99", date(1998, 7, 2)),
    ("Harry Potter and the Prisoner of Azkaban", "J. K. Rowling", 317, "10.99", date(1999, 7, 8)),
    ("Harry Potter and the Goblet of Fire", "J. K. Rowling", 636, "12.99", date(2000, 7, 8)),
    ("The Shining", "Stephen King", 447, "13.50", date(1977, 1, 28)),
    ("It", "Stephen King", 1138, "17.99", date(1986, 9, 15)),
    ("Misery", "Stephen King", 310, "11.00", date(1987, 6, 8)),
    ("The Green Mile", "Stephen King", 400, "12.00", date(1996, 3, 28)),
    ("11/22/63", "Stephen King", 849, "16.50", date(2011, 11, 8)),
]


class Command(BaseCommand):
    help = "Заполняет БД тестовыми авторами и книгами"

    def handle(self, *args, **options):
        Book.objects.all().delete()
        Author.objects.all().delete()

        authors = {
            name: Author.objects.create(name=name, country=country, birth_date=born)
            for name, country, born in AUTHORS
        }
        Book.objects.bulk_create(
            Book(title=t, author=authors[a], pages=p, price=Decimal(pr), published_date=d)
            for t, a, p, pr, d in BOOKS
        )
        self.stdout.write(self.style.SUCCESS(
            f"Создано авторов: {Author.objects.count()}, книг: {Book.objects.count()}"
        ))
