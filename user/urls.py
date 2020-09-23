from django.conf.urls import url
from user import views
from django.contrib import admin

urlpatterns = [
    url(r'^register', views.register),
    url(r'^login', views.login),
    url(r'^info', views.info)
]