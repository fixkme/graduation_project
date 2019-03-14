from django.db import models

# Create your models here.
class User(models.Model):
    nickname = models.CharField(max_length=16)
    phone = models.CharField(max_length=11)
    pwd = models.CharField(max_length=16)
