# Generated by Django 4.2.7 on 2024-03-29 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_book_customuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='count',
        ),
        migrations.AddField(
            model_name='book',
            name='isbn',
            field=models.IntegerField(blank=True, default=1954763259),
            preserve_default=False,
        ),
    ]
