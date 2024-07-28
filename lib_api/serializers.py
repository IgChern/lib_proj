from rest_framework import serializers
from lib_app.models import Book, BorrowedBook
from django.utils import timezone


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "authors", "genre"]


class BorrowedBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    days_on_hand = serializers.SerializerMethodField()

    class Meta:
        model = BorrowedBook
        fields = ["id", "book", "borrowed_date", "days_on_hand"]

    def get_days_on_hand(self, obj):
        if obj.returned_date:
            return (obj.returned_date - obj.borrowed_date).days
        else:
            return (timezone.now() - obj.borrowed_date).days
