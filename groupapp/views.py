from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
def register(request):

    return  render(request,'groupapp/register.html')


def registerlogic(request):

    pass


def login (request):
    return render(request,'groupapp/login.html')

def loginlogic(request):

    pass


def home(request):
    return  render(request,'groupapp/menu.html')

