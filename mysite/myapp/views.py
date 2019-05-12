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
    if request.method == "GET":
        try:
            pass
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
                user = User.objects.get(phone=val)
            else:
                user = User.objects.get(nickname=val)
            pwd = request.POST.get('pwd')
            if user.pwd == pwd: #登录成功，记录user信息
                request.session['logined'] = 1
                request.session['user_id'] = user.pk
                request.session['user_nickname'] = user.nickname
                request.session['user_figure'] = user.figure.url
                request.session['user_signature'] = user.signature
                request.session['user_cover'] = user.cover
                response = HttpResponseRedirect(reverse("index"))
                #response.set_cookie("user_id", user.pk, max_age=86400) #一天期限
                #response.set_cookie("user_figure", user.portrait, max_age=86400)  # 一天期限
                return response
            else:
                raise
        except:
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

def user(request):

    respond_data = {}
    try:
        user_id = request.session.get('user_id', None)
        m_user = User.objects.get(pk=user_id)
        respond_data['user_id'] = user_id
        respond_data['user_nickname'] = m_user.nickname
        respond_data['user_gender'] = m_user.get_gender_display()
        t = m_user.phone[3:7]
        respond_data['user_phone'] = m_user.phone.replace(t, '****')
        respond_data['user_signature'] = m_user.signature
        respond_data['user_figure'] = m_user.figure.url
        respond_data['user_cover'] = m_user.cover
    except Exception as err:
        print("user ---- ", err)

    if request.method == 'GET':
        album_list = []
        m_user = models.User.objects.get(pk=user_id)
        album_objs = models.Album.objects.filter(user=m_user)
        print("album_objs nums ---- ", len(album_objs))
        for obj in album_objs:
            data = {}
            photo_objs = models.Photo.objects.filter(album=obj)
            album_cover_obj = models.Photo.objects.get(cover=1, album=obj)
            album_tags = models.AlbumTag.objects.filter(album=obj).values_list('name', flat=True)
            print("{0} --- {1}".format(obj.name, len(photo_objs)))
            #print("url --- ", album_cover_obj.data.url)
            print("tags --- ", album_tags)

            data['photo_num'] = len(photo_objs)
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
                user = User.objects.get(pk=user_id)
                user_data['user_nickname'] = user.nickname
                user_data['user_figure'] = user.figure.url  #'/media/user_figures/default_profile.jpg'
                user_data['user_gender'] = user.gender
                user_data['user_signature'] = user.signature
                print(user_data['user_figure'])
                return HttpResponse(json.dumps(user_data))
            except Exception as err:
                print('setting load_user_data ----- ', err)
        elif op == "verify_nickname": #验证输入的昵称是否唯一
            ret = 't' #true
            val = request.GET.get('nickname')
            exist = User.objects.filter(nickname=val)
            if exist:
                ret = 'f' #false
            return HttpResponse(json.dumps({'ret':ret}))
        elif op == "verify_pwd": #验证输入的密码是否正确
            ret = 't' #true
            val = request.GET.get('old_pwd')
            user = User.objects.get(pk=user_id)
            if user.pwd != val:
                ret = 'f' #false
            return HttpResponse(json.dumps({'ret':ret}))

    return render(request, 'setting.html', respond_data)

#处理提交的个人资料修改
def alter_user_data(request):
    user_id = request.session.get('user_id', None)
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        user.nickname = request.POST.get('nickname', user.nickname)
        user.signature = request.POST.get('signature', user.signature)
        user.gender = request.POST.get('gender', user.gender)
        figure = request.FILES.get('imgInput', None)
        if figure:
            suffix = os.path.splitext(figure.name)[-1] #文件后缀
            dire = os.path.dirname(figure.name)
            file_name = os.path.join(dire, str(user_id) + suffix)
            figure.name = file_name
            user.figure = figure
        try:
            user.save()
            request.session['user_nickname'] = user.nickname
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
            m_user = User.objects.get(pk=user_id)
            album_name = request.POST.get('album_name', None)
            album_category = request.POST.get('album_category', None)
            album_note = request.POST.get('album_note', "")
            album_imgs = request.FILES.getlist('album_imgs', None)
            album_tags = request.POST.getlist('album_tags', None)
            album_cover = request.POST.get("album_cover", "0")
            print(len(album_imgs), len(album_tags))
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