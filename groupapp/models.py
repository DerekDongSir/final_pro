from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
    class Meta:
        db_table = 't_person'

# class Facepic(models.Model):
#     face_path = models.CharField(max_length=255)
#     owner = models.ForeignKey(to=Person,on_delete=models.CASCADE)
#     class Meta:
#         db_table = 't_facepic'
