from django.urls import path
from groupapp import views

app_name = 'groupapp'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('registerlogic/', views.registerlogic, name='registerlogic'),
    path('collectface/',views.collect_face,name='collectface'),
    path('login/', views.login, name='login'),
    path('loginlogic/', views.loginlogic, name='loginlogic'),
    path('phonelogin/', views.phonelogin, name='phonelogin'),
    path('phonelogic/', views.phonelogic, name='phonelogic'),
    path('facelogin/',views.facelogin,name='facelogin'),
    path('checkname/',views.check_name,name='checkname'),
    path('sendcode/', views.send_code, name='sendcode'),
    path('add_face/', views.add_user_face, name='face'),
    path('check_code/',views.check_code, name='check_code'),
]