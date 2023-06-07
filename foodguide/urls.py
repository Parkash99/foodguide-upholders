from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.view_index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('menu/', views.menu_view, name='menu'),
    path('order/', views.order_view, name='order'),
    path('place_order/', views.place_order_view, name='place_order'),
    path('order_success/', views.order_success, name='order_success'),
    path('rate-order/', views.rate_order, name='rate_order'),
    path('admin/', admin.site.urls),
    # Other URL patterns for your app
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
