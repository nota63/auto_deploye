"""
URL configuration for auto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from xml.etree.ElementInclude import include

from django.contrib import admin
from django.template.context_processors import static
from django.urls import path
from auto import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home,name='home'),
    path("main/",views.main,name='main'),
    path("google/",views.google,name='google'),
    path("birthday/",views.birthday,name='birthday'),
    path("success/",views.success,name='success'),
    path("youtube/",views.youtube,name='youtube'),
    path("playlists/",views.playlists,name='playlists'),
    path("info/",views.info,name='info'),
    path("email/",views.email,name='email'),
    path("emailSend/",views.emailSend,name='emailSend'),
    path("shutdown/",views.shutdown,name='shutdown'),
    path("system_info/",views.system_info,name='system_info'),
    path("speed/",views.speed,name='speed'),
    path("image/",views.image,name='image'),
    path("text_to_handwriting/",views.text_to_handwriting,name='text_to_handwriting'),
    path("whatsapp_image/",views.whatsapp_image,name='whatsapp_image'),
    path("multi_whatsapp/",views.multi_whatsapp,name='multi_whatsapp'),
    path("myself/",views.myself,name='myself'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)