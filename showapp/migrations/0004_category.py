# Generated by Django 2.0.6 on 2019-07-01 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showapp', '0003_auto_20190701_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('p_id', models.IntegerField(max_length=10)),
            ],
        ),
    ]
