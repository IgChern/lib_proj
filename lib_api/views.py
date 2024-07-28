from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from lib_app.models import Book, BorrowedBook
from .serializers import BookSerializer, BorrowedBookSerializer
from django.utils import timezone
from django.shortcuts import get_object_or_404


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.filter(available=True)
    serializer_class = BookSerializer


class BorrowedBookViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = BorrowedBook.objects.filter(
            user=request.user, returned_date__isnull=True
        )
        serializer = BorrowedBookSerializer(queryset, many=True)
        return Response(serializer.data)

    def borrow(self, request, pk=None):
        book = get_object_or_404(Book, id=pk)
        if book.available:
            BorrowedBook.objects.create(
                user=request.user, book=book, borrowed_date=timezone.now()
            )
            book.available = False
            book.save()
            return Response({"status": "book borrowed"}, status=status.HTTP_200_OK)
        return Response(
            {"status": "book not available"}, status=status.HTTP_400_BAD_REQUEST
        )

    def return_book(self, request, pk=None):
        borrowed_book = get_object_or_404(
            BorrowedBook, book_id=pk, user=request.user, returned_date__isnull=True
        )
        borrowed_book.returned_date = timezone.now()
        borrowed_book.save()
        borrowed_book.book.available = True
        borrowed_book.book.save()
        return Response({"status": "book returned"}, status=status.HTTP_200_OK)
