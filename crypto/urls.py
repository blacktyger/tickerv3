from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^stock/$', views.stock_redirect, name='stock_redirect'),
    path('', views.home, name="home"),

]


