"""Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers
from . import views
app_name ='authorization'

router = routers.DefaultRouter()
router.register(r'estado', views.EstadoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'signin/',
        views.signin,
        name='signin'
    ),
    path(
        'home/',
        views.home,
        name='home'
    ),
    path(
        'reportes/',
        views.reportes,
        name='reportes'
    ),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('transaccion/', views.Transaccion.as_view()),
    
]
