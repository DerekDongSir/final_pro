from django.shortcuts import render,HttpResponse,redirect
from .models import User
from django.db import transaction
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


def home(request):
    return  render(request,'groupapp/menu.html')

def huakuai_show(request):
    return render(request,'yangzhengma_huakuai/index.html')