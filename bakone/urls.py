from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('training/', views.training, name='training'),
    path('contact/', views.contact, name='contact'),
    # Secret admin dashboard path (change 'secure-admin-portal' to something unique)
    path('secure-admin-portal/', include('bakone.admin_dashboard.urls', namespace='admin_dashboard')),
    path('accounts/', include('django.contrib.auth.urls')),
]
