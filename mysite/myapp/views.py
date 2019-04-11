from django.shortcuts import render,render_to_response
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import json
from myapp.models import User
 

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.session.get('user_id', None):
        request.session.flush()
        return render(request,'index.html')
    if request.is_ajax():
        field = request.GET.get('field')
        ret = 't'
        exist = False
        if field == 'nickname':
            val = request.GET.get('nickname')
            exist = User.objects.filter(nickname=val)
        elif field == 'phone':
            val = request.GET.get('phone')
            exist = User.objects.filter(phone=val)
        if exist:
            ret = 'f'
        msg = {'msg':ret}
        return HttpResponse(json.dumps(msg))
    if request.method == 'POST':
        newUser = User()
        newUser.nickname = request.POST['nickname']
        newUser.phone = request.POST['phone']
        newUser.pwd = request.POST['pwd']
        newUser.save()
        return HttpResponseRedirect(reverse("login"))
    return render(request, 'register.html')


def login(request):
    if request.session.get('user_id', None):
        print("---------session[user_id]")
        request.session.flush()
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        val = request.POST.get('user')
        try:
            if len(val) == 11 and val.isdigit():
                user = User.objects.get(phone=val)
            else:
                user = User.objects.get(nickname=val)
            pwd = request.POST.get('pwd')
            if user.pwd == pwd:
                #request.session['user_id'] = user.pk
                return HttpResponseRedirect(reverse("index"))
            else:
                raise
        except:
            return render(request, 'login.html',
                         {'msg':'用户名或密码错误', 'username':val, 'pwd':pwd})
    return render(request, 'login.html')


def user(request):
    return render(request, 'user.html')

