from django.db import models

# Create your models here.


class Msg(models.Model):
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, null=True)
    age = models.CharField(max_length=20, null=True)
    hometown = models.CharField(max_length=20, null=True)
    living_place = models.CharField(max_length=20, null=True)
    ideal_position = models.CharField(max_length=40, null=True)
    ideal_city = models.CharField(max_length=60, null=True)
    salary = models.CharField(max_length=60, null=True)
    standby1 = models.CharField(max_length=20, null=True)
    standby2 = models.CharField(max_length=20, null=True)


class Category(models.Model):
    name = models.CharField(max_length=20)  # 城市名字和职位名字
    p_id = models.IntegerField()  #  城市 p_id 0  职位 p_id 1