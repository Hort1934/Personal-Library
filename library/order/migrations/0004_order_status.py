# Generated by Django 4.1 on 2023-07-14 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed')], default='Open', max_length=10),
        ),
    ]