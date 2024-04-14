from django.db import models
import book.models


class Author(models.Model):
    """
        Цей клас представляє Автора.
    """
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    books = models.ManyToManyField(book.models.Book, related_name='authors', blank=True)
    id = models.AutoField(primary_key=True)
    books = models.ManyToManyField('book.Book', related_name='author_books', blank=True)


    def __str__(self):
        # Возвращаем строку, которая состоит из имени и фамилии, разделенных пробелом
        return f"{self.name} {self.surname}"

    def __repr__(self):
        """
        Цей чарівний метод перевизначено так, щоб він показував клас та ідентифікатор об'єкта Author.
        """
        return f"Author(id={self.pk})"

    @staticmethod
    def get_by_id(author_id):
        try:
            return Author.objects.get(pk=author_id)
        except:
            return None

    @staticmethod
    def delete_by_id(author_id):
        try:
            author = Author.objects.get(pk=author_id)
            author.delete()
            return True
        except:
            return False

    @staticmethod
    def create(name, surname, patronymic):
        if name and len(name) <= 20 and surname and len(surname) <= 20 and patronymic and len(patronymic) <= 20:
            author = Author(name=name, surname=surname, patronymic=patronymic)
            author.save()
            return author

    def to_dict(self):
        pass

    def update(self,
               name=None,
               surname=None,
               patronymic=None):
        """
        Оновлює автора в базі даних із зазначеними параметрами.
        """

        if name and len(name) <= 20:
            self.name = name
        if surname and len(surname) <= 20:
            self.surname = surname
        if patronymic and len(patronymic) <= 20:
            self.patronymic = patronymic
        self.save()

    @staticmethod
    def get_all():
        """
        Повертає дані для json-запиту з QuerySet всіх авторів
        """
        return Author.objects.all()
