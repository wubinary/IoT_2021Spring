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

handler404 = 'ring.views.handler404'

# Device API
urlpatterns += [
    path('ring/regist_device/<str:mac_addr>', ring.regist_device), #註冊uid
    path('ring/need_update/<str:uid>/<str:git_version>', ring.need_update), #是否需要更新
    path('ring/success_update/<str:uid>/<str:git_version>', ring.success_update), #回報更新
    path('ring/i_am_alive/<str:uid>', ring.i_am_alive), #回報alive
]

# Web API
urlpatterns += [
    path('', ring.index),
    #path('ring/', ring.index),
    #path('ring/<str:uid>', ring.index),
    path('ring/ring_img/<str:uid>', ring.ring_image),
    path('ring/video_page_url/<str:uid>', ring.get_video_page_url),
    path('ring/knock/<str:uid>', ring.knock),
    path('ring/have_knock/<str:uid>', ring.have_knock),
    path('ring/unlock_page/<str:uid>', ring.unlock_page), #unlock page
    path('ring/login', ring.login), #login
    path('ring/logout', ring.logout), #logout
    path('ring/device_list', ring.device_list), #device list
    path('ring/get_abnormal_image/<str:uid>/<int:num>/<int:time>', ring.get_abnormal_image),
    path('ring/get_abnormal_time/<str:uid>/<int:num>/', ring.get_abnormal_time),
    path('ring/reply/<str:uid>', ring.ring_reply),
    path('ring/lock/<str:uid>', ring.lock),
    path('ring/anomaly/<str:uid>', ring.ring_anomaly),
    path('ring/have_anomaly/<str:uid>', ring.have_anomaly),

]

