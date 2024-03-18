from django.contrib import admin
from django.urls import path
from app import views


urlpatterns = [
  path('',views.home,name='home'),
  path('adminpanel',views.adminpanel),
  path('insert',views.insert),
  path('update/<id>',views.update),
  path('logoutAdmin', views.logoutAdmin, name='logoutAdmin'),
  path('adminlogin', views.adminlogin, name='adminlogin'),
  path('delete/<id>',views.delete),
  path('search',views.search),

  path('signup',views.handlesignup,name='handlesignup'),
  path('login',views.handlelogin,name='handlelogin'),
  path('logout',views.handlelogout,name='handlelogout'),


]
