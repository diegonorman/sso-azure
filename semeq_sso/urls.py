"""
URL configuration for semeq_sso project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from authentication import views as auth_views
from authentication import views

urlpatterns = [
    path('', auth_views.custom_login, name='root_login'),  # Redireciona / para login
    path('admin/', admin.site.urls),
    path('login/', auth_views.custom_login, name='login'),
    path('logout/', auth_views.custom_logout, name='logout'),
    path('dashboard/', auth_views.dashboard, name='dashboard'),
    path('sso/', include('djangosaml2.urls')),
    path('sso/acs', include('djangosaml2.urls')),  # Aceita POST sem barra final para compatibilidade total
    path('sso/error/', views.sso_error, name='sso_error'),
]
