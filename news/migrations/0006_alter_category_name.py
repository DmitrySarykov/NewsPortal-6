# Generated by Django 3.2.9 on 2022-02-02 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
