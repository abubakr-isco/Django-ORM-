# Django ORM — запросы к библиотеке

Модели `Author` и `Book`, запросы в `library/queries.py`:

1. **10 разных запросов** — функции `q01_…` … `q10_…`
2. **Lookups** — `__gt`, `__icontains`, `__in`, `__range`, `__year` (+ `__lt`, `__gte`, `__istartswith`, `Q`, `exclude`)
3. **Отчёт** — `authors_report()`: количество книг и средний объём у каждого автора (`annotate`)
4. **N+1** — 20 книг с авторами: **21 запрос** без `select_related` против **1** с ним

## Запуск

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_library   # тестовые данные
python manage.py run_queries    # вывод всех запросов
```
