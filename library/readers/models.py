from django.db import models


class Reader(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    # Додайте інші поля за необхідності, наприклад, адресу читача і т. д.

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
