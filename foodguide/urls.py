from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.view_index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('menu/', views.menu_view, name='menu'),
    path('admin/', admin.site.urls),
    # Other URL patterns for your app
]
