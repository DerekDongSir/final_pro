# Generated by Django 2.0.6 on 2019-07-01 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showapp', '0002_auto_20190701_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='msg',
            name='age',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='msg',
            name='gender',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='msg',
            name='hometown',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='msg',
            name='ideal_city',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='msg',
            name='ideal_position',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='msg',
            name='living_place',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='msg',
            name='salary',
            field=models.CharField(max_length=60, null=True),
        ),
    ]
