from django.urls import path
from groupapp import views

app_name = 'groupapp'
urlpatterns = [
    path('home/', views.home, name="home"),
    path('register/', views.register, name='register'),
    path('registerlogic/', views.registerlogic, name='registerlogic'),
    path('login/', views.login, name='login'),
    path('loginlogic/', views.loginlogic, name='loginlogic'),
    path('phonelogin/', views.phonelogin, name='phonelogin'),
    path('phonelogic/', views.phonelogic, name='phonelogic'),
    path('sendcode/', views.send_code, name='sendcode'),
    path('add_face/', views.add_user_face, name='face'),
]
