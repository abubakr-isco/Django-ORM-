"""
Домашнее задание: запросы к библиотеке (Author / Book).

Запуск:
    python manage.py run_queries
"""
from datetime import date

from django.db import connection, reset_queries
from django.db.models import Avg, Count, Max, Q

from .models import Author, Book


# ---------------------------------------------------------------------------
# 1–2. Десять разных запросов + минимум 5 разных lookups
# ---------------------------------------------------------------------------

def q01_thick_books():
    """__gt: книги толще 500 страниц."""
    return Book.objects.filter(pages__gt=500).order_by("-pages")


def q02_title_contains():
    """__icontains: в названии есть «harry» (без учёта регистра)."""
    return Book.objects.filter(title__icontains="harry")


def q03_authors_from_countries():
    """__in: авторы из России или Великобритании."""
    return Author.objects.filter(country__in=["Россия", "UK"]).order_by("name")


def q04_books_in_price_range():
    """__range: книги стоимостью от 10 до 15 (включительно)."""
    return Book.objects.filter(price__range=(10, 15)).order_by("price")


def q05_books_published_in_year():
    """__year: книги, изданные в 1869 году."""
    return Book.objects.filter(published_date__year=1869)


def q06_books_published_between_dates():
    """__range по датам: книги, изданные в XX веке."""
    return Book.objects.filter(
        published_date__range=(date(1901, 1, 1), date(2000, 12, 31))
    ).order_by("published_date")


def q07_short_books_of_russian_authors():
    """__lt + переход по связи author__country: короткие книги русских авторов."""
    return Book.objects.filter(pages__lt=200, author__country="Россия")


def q08_title_startswith_or_new():
    """Q-объекты + __istartswith / __year__gte: название на «the» ИЛИ изданы с 2000 года."""
    return Book.objects.filter(
        Q(title__istartswith="the") | Q(published_date__year__gte=2000)
    )


def q09_excluded_and_limited():
    """exclude + order_by + срез: 5 самых дешёвых книг, кроме Стивена Кинга."""
    return Book.objects.exclude(author__name="Stephen King").order_by("price")[:5]


def q10_authors_born_in_19th_century_with_long_books():
    """__year__lt + обратная связь books__pages__gte + distinct."""
    return Author.objects.filter(
        birth_date__year__lt=1900,
        books__pages__gte=800,
    ).distinct()


QUERIES = [
    q01_thick_books,
    q02_title_contains,
    q03_authors_from_countries,
    q04_books_in_price_range,
    q05_books_published_in_year,
    q06_books_published_between_dates,
    q07_short_books_of_russian_authors,
    q08_title_startswith_or_new,
    q09_excluded_and_limited,
    q10_authors_born_in_19th_century_with_long_books,
]


# ---------------------------------------------------------------------------
# 3. Отчёт: для каждого автора — количество книг и средний объём (annotate)
# ---------------------------------------------------------------------------

def authors_report():
    return Author.objects.annotate(
        books_count=Count("books"),
        avg_pages=Avg("books__pages"),
        max_pages=Max("books__pages"),
    ).order_by("-books_count", "name")


# ---------------------------------------------------------------------------
# 4. N+1: 20 книг с именами авторов — без и с select_related
# ---------------------------------------------------------------------------

def books_without_select_related(limit=20):
    reset_queries()
    lines = [f"{b.title} — {b.author.name}" for b in Book.objects.all()[:limit]]
    return lines, len(connection.queries)


def books_with_select_related(limit=20):
    reset_queries()
    lines = [
        f"{b.title} — {b.author.name}"
        for b in Book.objects.select_related("author")[:limit]
    ]
    return lines, len(connection.queries)


# ---------------------------------------------------------------------------
# Вывод всего в консоль
# ---------------------------------------------------------------------------

def run_all(out=print):
    out("=" * 70)
    out("1–2. ЗАПРОСЫ И LOOKUPS")
    out("=" * 70)
    for i, func in enumerate(QUERIES, start=1):
        out(f"\n{i}. {func.__doc__.strip()}")
        for obj in func():
            out(f"   - {obj}")

    out("\n" + "=" * 70)
    out("3. ОТЧЁТ ПО АВТОРАМ (annotate)")
    out("=" * 70)
    out(f"{'Автор':<22}{'Книг':>6}{'Ср. объём':>12}{'Макс.':>8}")
    for a in authors_report():
        out(f"{a.name:<22}{a.books_count:>6}{a.avg_pages or 0:>12.1f}{a.max_pages or 0:>8}")

    out("\n" + "=" * 70)
    out("4. N+1: 20 КНИГ С ИМЕНАМИ АВТОРОВ")
    out("=" * 70)
    lines, n_without = books_without_select_related()
    for line in lines:
        out(f"   {line}")
    _, n_with = books_with_select_related()
    out(f"\nБез select_related:  {n_without} SQL-запросов (1 + по одному на каждую книгу)")
    out(f"С select_related:    {n_with} SQL-запрос (JOIN author в одном запросе)")
