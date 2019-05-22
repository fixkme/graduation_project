from django.shortcuts import render,render_to_response
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import json, os
import myapp.models as models
from myapp.models import User, Photo

import myapp.tool as tool


def index(request):
    '''
    response_data = {}
    response_data["user_id"] = request.COOKIES.get('user_id')
    response_data["user_portrait"] = request.COOKIES.get('user_portrait')
    '''
    response_data = {}
    user_id = request.session.get('user_id', None)
    if request.method == "GET" and user_id:
        try:
            m_user = User.objects.get(pk=user_id)
            response_data['user_id'] = m_user.pk
            response_data['user_figure'] = m_user.figure.url
            return render(request, 'index.html', response_data)
        except Exception as err:
            print("index ------ ", err)
    return render(request, 'index.html')

def register(request):
    if request.session.get('logined', None):
        return render(request,'index.html')
    if request.is_ajax(): #注册验证
        field = request.GET.get('field')
        ret = 't' #ture
        exist = False
        if field == 'nickname':
            val = request.GET.get('nickname')
            exist = User.objects.filter(nickname=val)
        elif field == 'phone':
            val = request.GET.get('phone')
            exist = User.objects.filter(phone=val)
        if exist:
            ret = 'f' #false
        msg = {'msg':ret}
        return HttpResponse(json.dumps(msg))
    if request.method == 'POST': #注册成功，存储user信息
        try:
            newUser = User()
            newUser.nickname = request.POST['nickname']
            newUser.phone = request.POST['phone']
            newUser.pwd = request.POST['pwd']
            newUser.save()
            return HttpResponseRedirect(reverse("login"))
        except Exception as err:
            print("register ------ ",err)
    return render(request, 'register.html')


def login(request):
    if request.session.get('logined', None):
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        val = request.POST.get('user')
        try:
            if len(val) == 11 and val.isdigit():
                m_user = User.objects.get(phone=val)
            else:
                m_user = User.objects.get(nickname=val)
            pwd = request.POST.get('pwd')
            if m_user.pwd == pwd: #登录成功，记录user信息
                request.session['logined'] = 1
                request.session['user_id'] = m_user.pk
                request.session['user_nickname'] = m_user.nickname
                request.session['user_figure'] = m_user.figure.url
                request.session['user_signature'] = m_user.signature
                request.session['user_cover'] = m_user.cover
                response = HttpResponseRedirect(reverse("index"))
                #response.set_cookie("user_id", user.pk, max_age=86400) #一天期限
                #response.set_cookie("user_figure", user.portrait, max_age=86400)  # 一天期限
                return response
            else:
                raise
        except Exception as err:
            print("login ---- ", err)
            return render(request, 'login.html',
                         {'msg':'用户名或密码错误', 'username':val, 'pwd':pwd})
    return render(request, 'login.html')

def logout(request):
    if not request.session.get('logined', None):
        return render(request, 'index.html')
    request.session.flush()
    response = HttpResponseRedirect(reverse("index"))
    try:
        #response.delete_cookie("blog_username")
        #response.delete_cookie("blog_password")
        pass
    except Exception as err:
        print("logout ------ ", err)
    return response

def add(request, a):
    #c = int(a) + int(b)
    return HttpResponse(str(a))

def user(request, user_pk):

    user_id = request.session.get('user_id', None)
    respond_data = {}
    #return HttpResponse(str(user_pk))
    try:
        m_user = User.objects.get(pk=user_pk)
        respond_data['user_id'] = user_pk
        respond_data['user_nickname'] = m_user.nickname
        respond_data['user_gender'] = m_user.get_gender_display()
        t = m_user.phone[3:7]
        respond_data['user_phone'] = m_user.phone.replace(t, '****')
        respond_data['user_signature'] = m_user.signature
        respond_data['user_figure'] = m_user.figure.url
        respond_data['user_cover'] = m_user.cover
    except Exception as err:
        print("user ---- ", err)
        return render(request, 'user.html')
    #return HttpResponse(respond_data)
    if request.method == 'GET':
        album_list = []
        m_user = models.User.objects.get(pk=user_pk)
        album_objs = models.Album.objects.filter(user=m_user)
        print("album_objs nums ---- ", len(album_objs))
        for obj in album_objs:
            data = {}
            photo_objs = models.Photo.objects.filter(album=obj)
            album_cover_obj = models.Photo.objects.get(cover=1, album=obj)
            album_tags = models.AlbumTag.objects.filter(album=obj).values_list('name', flat=True)
            print("{0} --- {1}".format(obj.name, len(photo_objs)))
            #print("url --- ", album_cover_obj.data.url)
            #print("tags --- ", type(album_tags), album_tags)

            data['album_id'] = obj.pk
            data['album_photo_num'] = len(photo_objs)
            data['album_cover'] = album_cover_obj.data.url
            data['album_create_time'] = str(obj.create_time.date())
            data['album_name'] = obj.name
            data['album_tags'] = album_tags
            data['album_view_num'] = 0
            data['album_comment_num'] = 0
            data['album_favour_num'] = 0
            album_list.append(data)
        respond_data['album_list'] = album_list
        #print(album_list)
        return render(request, 'user.html', respond_data)
    '''
    if request.is_ajax():
        op = request.GET.get('op')
        print("user ---- ", op)
        if op == "load_user_data": #页面加载完获取个人信息
            user_data = {}
            m_user = User.objects.get(pk=user_id)
            user_data['user_id'] = user_id
            user_data['user_nickname'] = m_user.nickname
            user_data['user_gender'] = m_user.gender
            t = m_user.phone[3:7]
            user_data['user_phone'] = m_user.phone.replace(t, '****')
            user_data['user_signature'] = m_user.signature
            user_data['user_figure'] = m_user.figure.url
            user_data['user_cover'] = m_user.cover
            return HttpResponse(json.dumps(user_data))
    '''
    return render(request, 'user.html', respond_data)

def setting(request):
    respond_data = {}
    user_id = request.session.get('user_id', None)

    if request.is_ajax():
        op = request.GET.get('op')
        print('op : ', op)
        if op == "load_user_data": #页面加载完获取个人资料
            try:
                user_data = {}
                m_user = User.objects.get(pk=user_id)
                user_data['user_id'] = user_id
                user_data['user_nickname'] = m_user.nickname
                user_data['user_figure'] = m_user.figure.url
                user_data['user_gender'] = m_user.gender
                user_data['user_signature'] = m_user.signature
                #print(user_data['user_figure'])
                return HttpResponse(json.dumps(user_data))
            except Exception as err:
                print('setting load_user_data ----- ', err)
        elif op == "verify_nickname": #验证输入的昵称是否唯一
            try:
                ret = 't'  # true
                val = request.GET.get('nickname')
                exist = User.objects.get(nickname=val)
                if exist.pk != user_id:
                    ret = 'f'  # false
                return HttpResponse(json.dumps({'ret': ret}))
            except Exception as err:
                print("verify_nickname ----- ", err)
        elif op == "verify_pwd": #验证输入的密码是否正确
            try:
                ret = 't'  # true
                val = request.GET.get('old_pwd')
                m_user = User.objects.get(pk=user_id)
                if m_user.pwd != val:
                    ret = 'f'  # false
                return HttpResponse(json.dumps({'ret': ret}))
            except Exception as err:
                print("verify_pwd --- ", err)

    return render(request, 'setting.html', respond_data)

#处理提交的个人资料修改
def alter_user_data(request):
    user_id = request.session.get('user_id', None)

    if request.method == 'POST':
        try:
            m_user = User.objects.get(pk=user_id)
            m_user.nickname = request.POST.get('nickname', m_user.nickname)
            m_user.signature = request.POST.get('signature', m_user.signature)
            m_user.gender = request.POST.get('gender', m_user.gender)
            figure = request.FILES.get('imgInput', None)
            if figure:
                suffix = os.path.splitext(figure.name)[-1] #文件后缀
                dire = os.path.dirname(figure.name)
                file_name = os.path.join(dire, str(user_id) + suffix)
                figure.name = file_name
                m_user.figure = figure
                m_user.save()
                request.session['user_nickname'] = m_user.nickname
        except Exception as err:
            print('alter_user_data ---- ', err)
    return HttpResponseRedirect(reverse('setting'))

def alter_pwd(request):
    user_id = request.session.get('user_id', None)
    if request.method == 'POST':
        try:
            m_user = User.objects.get(pk=user_id)
            new_pwd = request.POST.get('newPwd')
            assert_pwd = request.POST.get('assertPwd')
            if new_pwd == assert_pwd:
                m_user.pwd = new_pwd
                m_user.save()
            else:
                raise ValueError("new_pwd != assert_pwd")
        except Exception as err:
            print('alter_user_data ---- ', err)
    return HttpResponseRedirect(reverse('setting'))

def issue(request):
    reponse_data = {}
    if request.method == 'POST':#request.is_ajax():
        reponse_data['ret'] = "上传成功"
        try:
            user_id = request.session.get('user_id')
            m_user = models.User.objects.get(pk=user_id)
            album_name = request.POST.get('album_name', '')
            album_category = request.POST.get('album_category', '')
            album_note = request.POST.get('album_note', "")
            album_imgs = request.FILES.getlist('album_imgs', [])
            album_tags = request.POST.getlist('album_tags', [])
            album_cover = request.POST.get("album_cover", "0")
            print(len(album_imgs), len(album_tags))
            if not album_imgs:
                raise Exception("没有上传图片，album_imgs is null！")
            new_album = models.Album()
            new_album.name = album_name
            new_album.category = album_category
            new_album.note = album_note
            new_album.user = m_user
            new_album.save()
            for i in range(len(album_imgs)):
                new_img = Photo()
                if i==int(album_cover):
                    new_img.cover = 1  #为相册封面
                new_img.name = album_imgs[i].name
                new_img.data = album_imgs[i]
                new_img.album = new_album
                new_img.save()
            for tag in album_tags:
                new_tag = models.AlbumTag()
                new_tag.name = tag
                new_tag.album = new_album
                new_tag.save()
        except Exception as err:
            print("issue ---- ", err)
            reponse_data['ret'] = "上传失败"
        return render(request, 'issue.html')
        #return HttpResponse(json.dumps(reponse_data))
    return render(request, 'issue.html')

def view_album(request, album_id):
    #print('view_album', album_id)
    response_data = dict()
    self_data = dict()
    user_data = dict()
    album_data = dict()
    user_id = request.session.get('user_id')
    try:
        m_user = models.User.objects.get(pk=user_id)
        album = models.Album.objects.get(pk=album_id)
        photos = models.Photo.objects.filter(album=album)#.values_list('data', flat=True)
        tags = models.AlbumTag.objects.filter(album=album).values_list('name', flat=True)

        album_photos_list = []
        for photo in photos:
            album_photos_list.append(photo.data.url)
        album_tags_list = []
        for tag in tags:
            album_tags_list.append(tag)

        user_data['user_id'] = m_user.pk
        user_data['user_nickname'] = m_user.nickname
        user_data['user_figure'] = m_user.figure.url
        user_data['user_signature'] = m_user.signature

        album_data['album_name'] = album.name
        album_data['album_create_time'] = str(album.create_time.date())
        album_data['album_category'] = album.get_category_display()
        album_data['album_note'] = album.note
        album_data['album_photo_num'] = len(photos)
        album_data['album_view_num'] = 1
        album_data['album_comment_num'] = 0
        album_data['album_favour_num'] = 0

        album_data['album_photos_list'] = album_photos_list
        album_data['album_tags_list'] = album_tags_list

        response_data['user_data'] = user_data
        response_data['album_data'] = album_data

        return render(request, 'view_album.html', response_data)
    except Exception as err:
        print("view_album " + str(album_id), err)
        return render(request, 'view_album.html')
