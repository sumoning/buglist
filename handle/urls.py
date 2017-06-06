#!/usr/bin/env python
#!_*_coding:utf-8_*_

from django.conf.urls import  url,include
from django.contrib.auth.views import login
import views

urlpatterns = [
    url(r'^accounts/login/',login,{'template_name':'login/login.html'}),
    url(r'^login/',views.Login),
    url(r'^logout/',views.Logout),
    url(r'^overview/',views.Overview),
    url(r'^deltails/(\d+)',views.Deltails),
    url(r'^record/',views.Record),
    url(r'^counts/',views.Counts),
    url(r'^search/',views.Search),
    url(r'^changpwd',views.Changpwd),
    url(r'^$',views.Index),
]
