from django.urls import path,re_path
from . import views

app_name = 'rango'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<category_name_slug>/add_page/',
         views.add_page, name='add_page'),
    # ?P<name>pattern ,named regular expression groups
    path('category/<category_name_slug>/',
         views.show_category, name='show_category'),
    # path('search/', views.search, name='search'),
    path('goto/', views.track_url, name='goto'),# 构造出重定向源URL
    path('register_profile/', views.register_profile, name='register_profile'),
    path('profile/<username>',views.profile,name='profile'),
    path('profiles/',views.list_profiles,name='list_profiles'),
    path('like_category/', views.like_category, name='like_category'),
    path('suggest/', views.suggest_category, name='suggest_category')

    # path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='login'),
    # path('restricted/', views.restricted, name='restricted'),
    # path('logout/', views.user_logout, name='logout'),
]
