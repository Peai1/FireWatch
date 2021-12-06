"""mapproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from map import views as map_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', map_views.mostrar_mapa, name='mostrar_mapa'),
    path('inicio/',map_views.inicio,name='inicio'),
    path('incendios/',map_views.incendios,name='incendios'),
    path("mapa/",map_views.ingresar_direccion,name='ingresar_direccion'),
    path("mapa1/",map_views.ubicacion_usuario,name='ubicacion_usuario'),
    path("mapa2/",map_views.puntero,name='puntero'),
    path("comments/",map_views.comentarios,name='comentarios'),
]
