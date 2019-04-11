from django.db import models

gender_choice = (
        (0, "保密"),
        (1,"男"),
        (2,"女"),
    )

# Create your models here.
class User(models.Model):
    nickname = models.CharField(max_length=16) #昵称
    pwd = models.CharField(max_length=16) #密码
    gender = models.IntegerField(choices=gender_choice, default=0) #性别
    phone = models.CharField(max_length=11)  #电话
    email = models.CharField(max_length=16, null=True)  #邮箱
    signature = models.CharField(max_length=50, null=True) #个人签名


