from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.view_index, name='index.html'),
    path('login/', views.view_login, name='login.html'),
    path('admin/', admin.site.urls),
]
