"""p1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls)
]

# Import view functions from ring app.
from ring import views as ring 

urlpatterns += [
    path('ring/', ring.index),
    path('ring/ring_img/', ring.ring_image),
    path('ring/video_page_url/', ring.get_video_page_url),
    path('ring/knock/', ring.knock),
    path('ring/have_knock/', ring.have_knock),
    path('ring/unlock_page/', ring.unlock_page),
    path('ring/get_abnormal_image/<int:num>/<int:time>', ring.get_abnormal_image),
    path('ring/get_abnormal_time/<int:num>/', ring.get_abnormal_time),
    path('ring/reply/', ring.ring_reply),
    path('ring/lock/', ring.lock),
    path('ring/anomaly/', ring.ring_anomaly),
    path('ring/have_anomaly/', ring.have_anomaly),

]

