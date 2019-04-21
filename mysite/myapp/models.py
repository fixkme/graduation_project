from django.db import models

default = {}
default['user_signature'] = "这个人很懒，什么都没写..."
default['user_portrait'] = "static/img/default_profile2.jpg"
default['user_cover'] = "static/img/3.jpg"

gender_choice = (
        (0, "保密"),
        (1,"男"),
        (2,"女"),
    )

# Create your models here.
class User(models.Model):
    nickname = models.CharField(max_length=16, unique=True) #昵称
    pwd = models.CharField(max_length=16) #密码
    phone = models.CharField(max_length=11)  # 电话

    gender = models.IntegerField(choices=gender_choice, default=0) #性别
    #email = models.CharField(max_length=16, null=True)  #邮箱
    signature = models.CharField(max_length=50, null=True, default="这个人很懒，什么都没写...") #个人签名
    portrait = models.CharField(max_length=50, null=True, default="/img/default_profile2.jpg") #头像路径
    cover = models.CharField(max_length=50, null=True, default="/img/3.jpg") #个人主页封面路径





