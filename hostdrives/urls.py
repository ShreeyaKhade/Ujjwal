from django.urls import path
from . import views

urlpatterns = [
    path("login/",views.login,name='login'),
    path("register/",views.register,name='register'),
    path("loginform/",views.loginform,name='loginform'),
    path("logout/",views.logout,name='logout'),
    path("joinlist/",views.joinlist,name='joinlist'),
    path("join/<int:id>",views.join,name='join'),
    path("withdraw/<int:id>",views.withdraw,name='withdraw'),
    path("host/",views.host,name='host'),
    path("rating/<int:id>",views.rating,name='rating'),
    path("",views.home,name='home')
]
