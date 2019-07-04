import re
import http.client
from urllib import parse
from django.shortcuts import render,HttpResponse,redirect
from .models import User
from django.db import transaction
from public_fun import Log

@Log
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

@Log
def login (request):
    return render(request,'groupapp/login.html')

@Log
def loginlogic(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        if User.objects.get(name=name,password=password):
            request.session['name'] = name
            return redirect('showapp:main')
    return redirect('groupapp:login')
@Log
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
    if re.match(r"^1(3|4|5|7|8)\d{9}$",phone) and User.objects.filter(phone=phone) : # 手机号格式相符并且在数据库中，才发短信
        code = send_sms(mobile=phone)  # 发送短信，获得短信码
        request.session[phone] = code # 将短信存入session,key为phone,value为code
        return HttpResponse('ok')
    return HttpResponse('no')
@Log
def phonelogic(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        code = request.POST.get('code')
        if request.session.get(phone) == code:
            return redirect('showapp:main')
    return redirect('groupapp:phonelogin')

