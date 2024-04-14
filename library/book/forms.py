from django.core.validators import MinValueValidator
from django import forms
from .models import Book
from author.models import Author


class BookFilterForm(forms.Form):
    author = forms.CharField(label='Author', required=False)
    genre = forms.CharField(label='Genre', required=False)
    year_of_publication = forms.IntegerField(label='Year of Publication', required=False)


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'description', 'isbn', 'date_of_issue', 'image', 'authors']

    # Додайте поле для зображення
    image = forms.ImageField(required=False, label='Image')
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all(), required=False, label='Authors')

    # # Якщо ви хочете додати валідатор для поля count, ви можете зробити це так
    # count = forms.IntegerField(validators=[MinValueValidator(0)])
