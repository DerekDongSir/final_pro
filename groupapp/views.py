import base64
import os
import re
import http.client
import time
from urllib import parse
from django.shortcuts import render,HttpResponse,redirect
from .models import User
from django.db import transaction
from groupapp.face_face import Face_to_Face as Fa

# Create your views here.
def register(request):
    return  render(request,'groupapp/register.html')


def registerlogic(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone= request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.get(phone=phone,email=email):
            return redirect('groupapp:register')
        with transaction.atomic():
            user = User(name=name,phone=phone,email=email,password=password)
            user.save()
            return redirect('groupapp:login')
    return redirect('groupapp:register')


def login (request):
    return render(request,'groupapp/login.html')

def loginlogic(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        if User.objects.get(name=name,password=password):
            return redirect('groupapp:home')
    return redirect('groupapp:login')

def phonelogin(request):
    return  render(request,'groupapp/phonelogin.html')

def send_sms(mobile,account  = 'C37538922',password = '50bcebbf62f2455d9483f9002fbc1781'):
    # 用户名是登录用户中心->验证码短信->产品总览->APIID
    # 密码 查看密码请登录用户中心->验证码短信->产品总览->APIKEY
    code = mobile[7:]
    text = "您的验证码是：" + code + "。请不要把验证码泄露给其他人。"
    host = "106.ihuyi.com"
    sms_send_uri = "/webservice/sms.php?method=Submit"
    params = parse.urlencode(
        {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    # conn = http.client.HTTPConnection(host, port=80, timeout=30)
    # conn.request("POST", sms_send_uri, params, headers)
    # response = conn.getresponse()
    # response_str = response.read()
    # conn.close()
    return code



def send_code(request):
    phone = request.GET.get('phone')
    if re.match(r"^1(3|4|5|7|8)\d{9}$",phone):
        code = send_sms(mobile=phone)  # 发送短信，获得短信码
        request.session[phone] = code # 将短信存入session,key为phone,value为code
        return HttpResponse('ok')
    return HttpResponse('no')

def phonelogic(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        code = request.POST.get('code')
        if request.session.get(phone) == code:
            return redirect('groupapp:home')
    return redirect('groupapp:phonelogin')

def home(request):
    return  render(request,'groupapp/menu.html')

def add_user_face(request):
    name = request.POST.get('name')
    mana=request.POST.get('mana')
    fa_im = request.POST.get('pp').replace("data:image/jpeg;base64,", "")
    num = request.POST.get('um')
    img = base64.b64decode(fa_im)
    try:
        with open(str(num)+'.jpg','bw') as b:
            b.write(img)
            b.close()
        if mana == 'add':
            face = Fa('user_face', 'user_face').add_face(name, str(num)+'.jpg')
        else:
            face = Fa('user_face', 'user_face').face_yanzheng(name,str(num)+'.jpg',0.35)
        os.remove(str(num) + '.jpg')
        if face:
            return HttpResponse('1')
        else:
            return HttpResponse('0')
    except:
        return HttpResponse('0')
