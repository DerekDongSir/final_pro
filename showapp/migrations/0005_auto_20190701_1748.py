# Generated by Django 2.0.6 on 2019-07-01 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showapp', '0004_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='p_id',
            field=models.IntegerField(),
        ),
    ]
