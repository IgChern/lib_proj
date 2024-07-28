from django.urls import path
from .views import (
    LoginUser,
    SignUpView,
    BookListView,
    BorrowOrReturnBookView,
    MyBooksView,
    HoldersView,
)
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

app_name = "lib"

urlpatterns = [
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("catalog/", login_required(BookListView.as_view()), name="catalog"),
    path(
        "borrow_or_return/<int:book_id>/",
        BorrowOrReturnBookView.as_view(),
        name="borrow_or_return",
    ),
    path("my_books/", login_required(MyBooksView.as_view()), name="my_books"),
    path("holders/", login_required(HoldersView.as_view()), name="holders"),
]
