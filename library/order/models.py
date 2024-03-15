from django.db import models, DataError
from authentication.models import CustomUser
from book.models import Book


class Order(models.Model):
    """
       This class represents an Order.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(default=None, null=True, blank=True)
    plated_end_at = models.DateTimeField(default=None)

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Open')

    def __str__(self):
        """
        Magic method is redefined to show all information about Book.
        """
        if self.end_at is None:
            return f"\'id\': {self.pk}, " \
                   f"\'user\': CustomUser(id={self.user.pk})," \
                   f" \'book\': Book(id={self.book.pk})," \
                   f" \'created_at\': \'{self.created_at}\'," \
                   f" \'end_at\': {self.end_at}," \
                   f" \'plated_end_at\': \'{self.plated_end_at}\'"
        else:
            return f"\'id\': {self.pk}, " \
                   f"\'user\': CustomUser(id={self.user.pk})," \
                   f" \'book\': Book(id={self.book.pk})," \
                   f" \'created_at\': \'{self.created_at}\'," \
                   f" \'end_at\': \'{self.end_at}\'," \
                   f" \'plated_end_at\': \'{self.plated_end_at}\'"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Book object.
        """
        return f'{self.__class__.__name__}(id={self.id})'

    def to_dict(self):
        pass

    @staticmethod
    def create(user, book, plated_end_at):
        orders = Order.objects.all()
        books = set()
        for order in orders:
            if not order.end_at:
                books.add(order.book.id)
        if book.id in books and book.count == 1:
            return None
        try:
            order = Order(user=user, book=book, plated_end_at=plated_end_at)
            order.save()
            return order
        except ValueError:
            return None
        except DataError:
            return None

    @staticmethod
    def get_by_id(order_id):
        try:
            return Order.objects.get(pk=order_id)
        except:
            return None

    def update(self, plated_end_at=None, end_at=None):
        if plated_end_at != None:
            self.plated_end_at = plated_end_at
        if end_at != None:
            self.end_at = end_at
        self.save()

    @staticmethod
    def get_all():
        return list(Order.objects.all())

    @staticmethod
    def get_not_returned_books():
        return Order.objects.filter(end_at=None).values()

    @staticmethod
    def delete_by_id(order_id):
        try:
            a = Order.objects.get(pk=order_id)
        except:
            return False
        else:
            a.delete()
            return True


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=256, blank=True)
    count = models.IntegerField(default=10)
    date_of_issue = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class CustomUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=254, unique=True)
