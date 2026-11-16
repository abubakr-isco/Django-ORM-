from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    pages = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    published_date = models.DateField()

    def __str__(self):
        return self.title
