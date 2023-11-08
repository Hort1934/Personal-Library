from django import forms
from django.core.validators import MinValueValidator

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date', 'Count']

    class BookForm(forms.ModelForm):
        Count = forms.IntegerField(validators=[MinValueValidator(0)])
