# Generated by Django 4.0.2 on 2022-03-01 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0002_item_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
