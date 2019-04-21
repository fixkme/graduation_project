from django.shortcuts import render,render_to_response
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import json
from myapp.models import User
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
                request.session['user_portrait'] = user.portrait
                request.session['user_signature'] = user.signature
                request.session['user_cover'] = user.cover
                response = HttpResponseRedirect(reverse("index"))
                response.set_cookie("user_id", user.pk, max_age=86400) #一天期限
                response.set_cookie("user_portrait", user.portrait, max_age=86400)  # 一天期限

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

    respond_data = {
        "user_nickname" : request.session['user_nickname'],
        "user_signature" : request.session['user_signature'],
        "user_portrait" : request.session['user_portrait'],
        "user_cover":request.session['user_cover'],
    }

    '''
    if request.method == 'GET':
        try:
            pass
        except Exception as err:
            pass
    '''
    return render(request, 'user.html', respond_data)

def setting(request):
    respond_data = {}
    user_id = request.session.get('user_id', None)

    if request.is_ajax():
        op = request.GET.get('op')
        print(op)
        if op == "load_form_ajax": #页面加载完获取个人资料
            user_data = {}
            user = User.objects.get(pk=user_id)
            user_data['user_nickname'] = user.nickname
            user_data['user_portrait'] = user.portrait
            user_data['user_gender'] = user.gender
            user_data['user_signature'] = user.signature
            #print(user_data)
            return HttpResponse(json.dumps(user_data))
        elif op == "input_nickname": #验证输入的昵称是否唯一
            ret = 't' #true
            val = request.GET.get('nickname')
            exist = User.objects.filter(nickname=val)
            if exist:
                ret = 'f' #false
            return HttpResponse(json.dumps({'ret':ret}))
    return render(request, 'setting.html', respond_data)

#处理提交的个人资料修改
def setting_profile(request):
    pass