from django.core.validators import MinValueValidator

from .models import Book

from django import forms


class BookFilterForm(forms.Form):
    author = forms.CharField(label='Author', required=False)
    genre = forms.CharField(label='Genre', required=False)
    year_of_publication = forms.IntegerField(label='Year of Publication', required=False)


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date', 'Count']

    class BookForm(forms.ModelForm):
        Count = forms.IntegerField(validators=[MinValueValidator(0)])
