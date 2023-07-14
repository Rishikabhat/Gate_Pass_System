"""GatePassManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from collegegatepass.views import login, registration, logout, loginpage, getpassrequests, deletepassrequest, \
    addpassrequest, approveorrejectrequest, recognizeuser, departmentloginaction

urlpatterns = [

    path('admin/', admin.site.urls),

    path('',TemplateView.as_view(template_name = 'index.html'),name='login'),
    path('login/',loginpage,name='login'),
    path('loginaction/',login,name='loginaction'),
    path('registration/',TemplateView.as_view(template_name = 'registration.html'),name='registration'),
    path('regaction/',registration,name='regaction'),
    path('logout/', logout, name='logout'),

    path('approveorrejectrequest/',approveorrejectrequest,name='activateAccount'),

    path('addpassrequest/',TemplateView.as_view(template_name ='addpassrequest.html'),name='apply'),
    path('addpassrequestaction/',addpassrequest,name='apply'),
    path('getpassrequests/',getpassrequests,name='add'),
    path('deletepassrequest/',deletepassrequest,name='delete'),
    path('recognizeuser/',recognizeuser,name='delete'),

    path('departmentlogin/',TemplateView.as_view(template_name ='departmentlogin.html'),name='apply'),
    path('departmentloginaction/',departmentloginaction,name='loginaction'),
]
