from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class Librarian(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    staff_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    GENDER_OPTIONS = (
        ("f", "Женский"),
        ("m", "Мужской"),
        ("n", "Не указан"),
    )
    gender = models.CharField(
        max_length=1, choices=GENDER_OPTIONS, default="n", blank=True
    )
    address = models.TextField(blank=True, default="")

    def __str__(self):
        return self.user.username


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField("Author", related_name="books")
    genre = models.ManyToManyField("Genre", related_name="books")
    available = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    GENRE_OPTIONS = (
        ("Fic", "Худ лит-ра"),
        ("Mys", "Мистика"),
        ("Thr", "Триллер"),
        ("Fan", "Фэнтези"),
        ("Rom", "Роман"),
        ("His", "История"),
    )
    genre_name = models.CharField(max_length=3, choices=GENRE_OPTIONS, blank=True)

    def __str__(self) -> str:
        return self.genre_name


class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.user.username} взял {self.book.title}"
