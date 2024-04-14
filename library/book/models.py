from django.db import models


class User(models.Model):
    """
    This class represents a user.
    """
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

    def get_all_books(self):
        """
        Get all books provided to this user.
        """
        return self.books_provided.all()


from django.db import models

class Book(models.Model):
    """
        This class represents a Book.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=256, blank=True)
    date_of_issue = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)  # Поле для зображення
    isbn = models.CharField(max_length=13, blank=True)  # Поле для ISBN
    authors = models.ManyToManyField('author.Author', related_name='book_authors', blank=True)
    link = models.URLField(max_length=200, blank=True)  # Поле для URL посилання

    def __str__(self):
        """
        Повертає рядок, що описує книгу.
        """
        authors = [author.id for author in self.authors.all()]
        return f"{self.name[:20]}"

    def __repr__(self):
        """
        Повертає текстовий опис об'єкта книги.
        """
        return f"Book(id={self.id})"

    @staticmethod
    def get_by_id(book_id):
        """
        Повертає книгу за її ID.
        """
        return Book.objects.get(id=book_id) if Book.objects.filter(id=book_id) else None

    @staticmethod
    def delete_by_id(book_id):
        """
        Видаляє книгу за її ID.
        """
        if Book.get_by_id(book_id) is None:
            return False
        Book.objects.get(id=book_id).delete()
        return True

    @staticmethod
    def create(name, description, authors=None, link=None):
        """
        Створює нову книгу та додає її до бази даних.
        """
        if len(name) > 128:
            return None

        book = Book()
        book.name = name
        book.description = description
        if authors:
            for elem in authors:
                book.authors.add(elem)
        if link:
            book.link = link
        book.save()
        return book

    def to_dict(self):
        """
        Повертає словник з інформацією про книгу.
        """
        # Implement this method based on your requirements.

    def update(self, name=None, description=None, link=None):
        """
        Оновлює інформацію про книгу.
        """
        if name is not None:
            self.name = name

        if description is not None:
            self.description = description

        if link is not None:
            self.link = link

        self.save()

    def add_authors(self, authors):
        """
        Додає авторів до книги.
        """
        if authors:
            for elem in authors:
                self.authors.add(elem)
                self.save()

    def remove_authors(self, authors):
        """
        Видаляє авторів з книги.
        """
        for elem in authors:
            self.authors.remove(elem)
            self.save()

    @staticmethod
    def get_all():
        """
        Повертає список усіх книг.
        """
        return list(Book.objects.all())
