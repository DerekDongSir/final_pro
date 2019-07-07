from django.urls import path
from showapp import views

app_name = 'showapp'

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('main/', views.main, name='main'),
    path('introduce/', views.introduce, name='introduce'),
    path('changePage/',views.changePage,name='changePage'),
    path('jumpPage/',views.jumpPage,name='jumpPage'),
    path('searchMsg/',views.searchMsg,name='searchMsg'),
    path('city_map/',views.city_map,name = 'city_map'),
    path('open_city_map/',views.open_city_map)
]


