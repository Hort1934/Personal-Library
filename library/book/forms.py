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
        fields = ['name', 'description', 'count', 'date_of_issue', 'image']

    # Добавьте поле для изображения
    image = forms.ImageField(required=False, label='Image')

    # Если вы хотите добавить валидатор для поля count, вы можете сделать это так
    count = forms.IntegerField(validators=[MinValueValidator(0)])
