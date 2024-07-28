from django.contrib import admin
from .models import Librarian, Student, Book, Author, Genre, BorrowedBook


@admin.register(BorrowedBook)
class BorAdm(admin.ModelAdmin):
    list_display = ("id", "borrowed_date", "returned_date")
    list_filter = ("returned_date",)
    search_fields = ("user__username", "book__title")


@admin.register(Librarian)
class LibrAdm(admin.ModelAdmin):
    search_fields = ("staff_number",)
    list_display = (
        "staff_number",
        "user",
    )


@admin.register(Student)
class StudAdm(admin.ModelAdmin):
    search_fields = ("address",)
    list_display = (
        "address",
        "user",
    )


@admin.register(Book)
class BookAdm(admin.ModelAdmin):
    search_fields = ("title",)
    list_display = ("title",)


@admin.register(Author)
class AuthorAdm(admin.ModelAdmin):
    search_fields = ("id", "name")
    list_display = ("id", "name")


@admin.register(Genre)
class GenreAdm(admin.ModelAdmin):
    search_fields = ("id", "genre_name")
    list_display = ("id", "genre_name")
