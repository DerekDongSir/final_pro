from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
