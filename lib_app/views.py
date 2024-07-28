from .models import Book, BorrowedBook
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import LoginUserForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic import ListView, View


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "lib_app/login.html"

    def get_success_url(self):
        if hasattr(self.request.user, "librarian") and self.request.user.librarian:
            return reverse_lazy("lib:holders")
        else:
            return reverse_lazy("lib:catalog")


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("lib:catalog")
    template_name = "lib_app/signup.html"


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = "lib_app/catalog.html"
    context_object_name = "books"
    paginate_by = 5

    def get_queryset(self):
        return Book.objects.filter(available=True).order_by("title")


class BorrowOrReturnBookView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        borrowed_book, created = BorrowedBook.objects.get_or_create(
            user=request.user, book=book, returned_date__isnull=True
        )
        if not created and borrowed_book.user != request.user:
            return redirect("lib:catalog")
        if created:
            book.available = False
            book.save()
        else:
            borrowed_book.returned_date = timezone.now()
            borrowed_book.save()
            book.available = True
            book.save()
        return redirect("lib:catalog")


class MyBooksView(LoginRequiredMixin, ListView):
    model = BorrowedBook
    template_name = "lib_app/my_books.html"
    context_object_name = "my_books"

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, "librarian") and request.user.librarian:
            return redirect("lib:holders")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return BorrowedBook.objects.filter(user=self.request.user).order_by("book")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        for borrowed_book in context["my_books"]:
            if borrowed_book.returned_date:
                borrowed_book.days_on_hand = (
                    borrowed_book.returned_date - borrowed_book.borrowed_date
                ).days
            else:
                borrowed_book.days_on_hand = (now - borrowed_book.borrowed_date).days
        return context


class HoldersView(LoginRequiredMixin, ListView):
    model = BorrowedBook
    template_name = "lib_app/holders.html"
    context_object_name = "holders"

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "librarian") or not request.user.librarian:
            return redirect("lib:my_books")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return BorrowedBook.objects.filter(returned_date__isnull=True).order_by(
            "borrowed_date"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        for holder in context["holders"]:
            if holder.returned_date:
                holder.days_on_hand = (holder.returned_date - holder.borrowed_date).days
            else:
                holder.days_on_hand = (now - holder.borrowed_date).days
        return context
