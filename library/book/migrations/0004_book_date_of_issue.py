# Generated by Django 4.1 on 2023-07-11 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='date_of_issue',
            field=models.DateField(blank=True, null=True),
        ),
    ]
