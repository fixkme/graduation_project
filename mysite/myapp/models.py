
from django.db import models
from django.utils import timezone
import os
#from myapp.tool import FigureImageStorage, ImageStorage

gender_choice = (
    (0, "保密"),
    (1, "男"),
    (2, "女"),
)

access_rank =(
    (0, "所有人"),
    (1, "关注的人"),
    (2, "仅自己"),
)

copyright_rank = (
    (0, "随意"),
    (1, "不能下载"),
)

album_category_choice = (
        (0, "生活"),
        (1, "人像"),
        (2, "插画"),
        (3, "二次元"),
        (4, "设计"),
        (5, "美食"),
        (6, "纪实"),
        (7, "风景"),
        (8, "其他"),
)

def user_photo_directory(instance, filename):
    user_id = instance.album.user.pk
    return os.path.join("photo", str(user_id),  filename) #/media/1/avatar/


# Create your models here.
class User(models.Model):
    nickname = models.CharField(max_length=16, unique=True) #昵称
    pwd = models.CharField(max_length=16) #密码
    phone = models.CharField(max_length=11)  # 电话
    gender = models.IntegerField(choices=gender_choice, default=0) #性别
    signature = models.CharField(max_length=50, null=True, default="这个人很懒，什么都没写...") #个人签名
    cover = models.CharField(max_length=50, null=True, default="/static/img/3.jpg") #个人主页封面路径
    #portrait = models.CharField(max_length=50, null=True, default="/static/img/default_profile.jpg")  # 头像路径
    figure = models.ImageField(upload_to='user_figures', null=True, default="/default_profile.jpg")

class Album(models.Model):
    name = models.CharField(max_length=16)
    category = models.IntegerField(choices=album_category_choice, default=0) #类别
    note = models.TextField(null=True, blank=True) #描述
    create_time = models.DateTimeField(default=timezone.now)  #
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #拥有者

class Photo(models.Model):
    name = models.CharField(max_length=50) #
    data = models.ImageField(upload_to=user_photo_directory)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    cover = models.IntegerField(default=0) #是否为album的封面
    label = models.IntegerField(null=True, blank=True)

class AlbumTag(models.Model): #相册的标签
    name = models.CharField(max_length=8) #
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

#---- <社交
class Collection(models.Model): #收藏
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)

class Favour(models.Model): #点赞
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)

class AlbumComment(models.Model): #评论
    content = models.CharField(max_length=1000) #评论内容
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    origin_comment = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)  #父级评论
    user = models.ForeignKey(User, null=False,on_delete=models.CASCADE)
    time = models.DateTimeField(null=True, default=timezone.now)

#---- 社交>
