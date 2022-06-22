from django.urls import path
from . import views
from .views import *
from . import views

urlpatterns=[
    path("home",home,name="home"),
    path("login/",views.Login,name="Login"),
    path("loginUser/",views.loginFunc,name="loginFunc"),
    path("post-user",views.postUser,name="postUser"),
    path('posts/',PostAPI.as_view()),
    path('my-posts/',views.MyPosts,name="MyPosts"),
    path('register/',RegisterUser.as_view()),
    path('update/',PostAPI.as_view()),
]


