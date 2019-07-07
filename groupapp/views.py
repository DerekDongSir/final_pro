import base64
import hashlib
import os
import random
import re
import http.client
import string
import uuid
from urllib import parse
from django.shortcuts import render, HttpResponse, redirect
from .models import Person
from django.db import transaction
from groupapp.face_face import Face_to_Face as Fa


# Create your views here.
def register(request):
    return render(request, 'groupapp/register.html')


def registerlogic(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if Person.objects.filter(name=name):  # 用户名需要唯一
            return redirect('groupapp:register')
        with transaction.atomic():
            user = Person(name=name, phone=phone, email=email, password=password)
            user.save()
            request.session['name'] = name  # 将注册后的name存入cookie,便于人脸识别时使用
            return redirect('groupapp:collectface')
    return redirect('groupapp:register')


def collect_face(request):
    if request.session.get('name'):
        return render(request, 'groupapp/collect_face.html')
    return redirect('groupapp:register')  # 如果session中不存在用户名信息，返回注册页面


def login(request):
    status = request.GET.get('status')  # 如果时从人脸识别部分进行登录，会传递状态参数
    if status == '1':
        name = request.session.get('name')
        user = Person.objects.get(name=name)
        user.status = 1
        user.save()
    return render(request, 'groupapp/login.html')


def loginlogic(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        # print(request.session.get('code'))
        # print(request.COOKIES['code'])
        if code_to_code(request, code):
            return HttpResponse('none')
        name = request.POST.get('name')
        user = Person.objects.filter(name=name)
        if not user:  # 用户名查询不到，返回用户注册页面
            return HttpResponse('name_error')
        else:  # 用户名能够查询到

            if not user.status:  # 人脸识别状态未被激活，返回人脸采集页面
                request.session['name'] = name  # 将用户名保存进cookie
                return redirect('face')
            password = request.POST.get('password')  # 状态处于被激活状态，取密码进行验证
            if Person.objects.get(name=name, password=password):
                return HttpResponse('ok')
            return HttpResponse('pwd_error') # 密码错误，继续登录
    return HttpResponse('none')


def phonelogin(request):
    return render(request, 'groupapp/phonelogin.html')


def facelogin(request):
    return render(request, 'groupapp/facelogin.html')


def check_name(request):
    name = request.GET.get('name')
    if Person.objects.filter(name=name):
        user = Person.objects.get(name=name)
        if user.status:  # 有名可查，且状态已被激活，
            return HttpResponse('1')  # 允许人脸识别登录
        request.session['name'] = name  # 将name存入cookie,便于下一步人脸信息采集
        return HttpResponse('2')  # 返回到人脸收集页面
    return HttpResponse('3')  # 返回到注册页面。


def send_sms(mobile, account='C37538922', password='50bcebbf62f2455d9483f9002fbc1781'):
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
    if re.match(r"^1(3|4|5|7|8)\d{9}$", phone):
        code = send_sms(mobile=phone)  # 发送短信，获得短信码
        request.session[phone] = code  # 将短信存入session,key为phone,value为code
        return HttpResponse('ok')
    return HttpResponse('no')


def phonelogic(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        code = request.POST.get('code')
        if request.session.get(phone) == code:
            return redirect('showapp:main')
    return redirect('groupapp:phonelogin')


def add_user_face(request):
    name = request.session.get('name')
    if not name:
        return HttpResponse('2')  # 用户名不存在，返回到注册页面
    mana = request.POST.get('mana')
    fa_im = request.POST.get('pp').replace("data:image/jpeg;base64,", "")
    num = request.POST.get('um')
    img = base64.b64decode(fa_im)
    try:
        with open(str(num) + '.jpg', 'bw') as b:
            b.write(img)
            b.close()
        if mana == 'add':
            face = Fa('user_face', 'user_face').add_face(name, str(num) + '.jpg')
        else:
            face = Fa('user_face', 'user_face').face_yanzheng(name, str(num) + '.jpg', 0.35)
        os.remove(str(num) + '.jpg')
        if face:
            return HttpResponse('1')
        else:
            return HttpResponse('0')
    except:
        return HttpResponse('0')


def check_code(request):
    session_dict = request.session['code']
    if isinstance(session_dict,dict):
        session_dict = {}
    cod = random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, 16)
    random_code = "".join(cod)
    name = str(uuid.uuid4())
    res = HttpResponse(random_code)
    session_dict.update({name: random_code})
    request.session['code']=session_dict
    res.set_cookie('code',name,max_age=100)
    return res
#
def code_to_code(request,check_num):
    code_name = request.COOKIES['code']
    code = request.session.get('code')[code_name]
    h = hashlib.md5()
    h.update(code.encode())
    if h.hexdigest() == check_num:
        return True
    else:
        return False
