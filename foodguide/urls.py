from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.view_index, name='index'),  # URL pattern for the index page
    path('login/', views.login_view, name='login'),  # URL pattern for the login page
    path('signup/', views.signup_view, name='signup'),  # URL pattern for the signup page
    path('logout/', views.logout_view, name='logout'),  # URL pattern for the logout functionality
    path('dashboard/', views.dashboard_view, name='dashboard'),  # URL pattern for the dashboard page
    path('menu/', views.menu_view, name='menu'),  # URL pattern for the menu page
    path('order/', views.order_view, name='order'),  # URL pattern for the order page
    path('place_order/', views.place_order_view, name='place_order'),  # URL pattern for placing an order
    path('order_success/', views.order_success, name='order_success'),  # URL pattern for the order success page
    path('rate-order/', views.rate_order, name='rate_order'),  # URL pattern for rating an order
    path('admin/', admin.site.urls),  # URL pattern for the Django admin site
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
