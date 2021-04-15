from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.core.files import File 
from datetime import datetime, timedelta
from django.utils import timezone
from .models import (
    User,
    Abnormal_Image,
    Device,
    Knock,
    Unlock,
    Version,
    VersionLog,
    Cookie,
)
import json
from multiprocessing import Process 
from django.shortcuts import redirect
from django.http import JsonResponse
from random_username.generate import generate_username

#404 page
def handler404(request, exception):
    return HttpResponse('404 not found')

#首頁redirect to /ring/unlock_page/<uid>
def index(request, uid=None):
    return redirect(f'/ring/login')

#註冊uid
def regist_device(request, mac_addr):
    candidates = Device.objects.filter(mac_addr=mac_addr)
    if len(candidates) == 0: 
        # regist new mac_addr
        nick_name = generate_username(1)[0]
        version = Version.objects.last()
        device = Device.objects.create(nick_name = nick_name,
                                       mac_addr = mac_addr, 
                                       version = version,
                                       update_to_version = version)
        path = f'/home/iot/Desktop/iot_project/p2/server/tmp/{device.uid}'
        if not os.path.exists(path):
            os.makedirs(path)
        os.system(f'chmod -R 777 {path}')
    else: 
        # mac_addr have already registed
        device = candidates[0]
    response_dict = {
        'message': "Success Registed!!",
        'MAC': device.mac_addr,
        'UID': device.uid 
    }
    return JsonResponse(response_dict)

#詢問是否需要update
def need_update(request, uid, git_version):
    # uid not found
    if not Device.objects.filter(uid=uid).exists():
        response_dict = {
            'message': f'uid {uid} not found'
        }
        return JsonResponse(response_dict)
    device = Device.objects.filter(uid=uid)[0]
    # first version
    if git_version=='00000' or not Version.objects.filter(git_version=git_version).exists():
        newer_versions = Version.objects.all().order_by('-timestamp')
        newer_git_versions = [{'git_repo': v.git_repo,
                               'git_version': v.git_version} for v in newer_versions]
        response_dict = {
            'message': f'There are {len(newer_git_versions)} newer versions',
            'git_version': device.version.git_version,
            'newer_git_versions': newer_git_versions 
        }
        return JsonResponse(response_dict)
    version = Version.objects.filter(git_version=git_version)[0]
    # keep newest
    if device.keep_newest:
        newer_versions = Version.objects.filter(
                            timestamp__gt=version.timestamp).order_by('-timestamp')
        newer_list = [{'git_repo': v.git_repo,
                       'git_version': v.git_version} for v in newer_versions]
        
        response_dict = {
            'message': f'There are {len(newer_list)} newer versions',
            'git_version': device.version.git_version,
            'newer_git_versions': newer_list  
        }
        return JsonResponse(response_dict)
    # update to version
    if Version.objects.filter(git_version=git_version).exists() and git_version!=device.update_to_version.git_version:
        update_to_version = Version.objects.filter(
                                git_version=device.update_to_version.git_version)[0]
        newer_list = [{'git_repo': update_to_version.git_repo, 
                       'git_version': update_to_version.git_version}]
        
        response_dict = {
            'message': f'There are {len(newer_list)} newer versions',
            'git_version': device.version.git_version,
            'newer_git_versions': newer_list
        }
        return JsonResponse(response_dict)
    
    response_dict = {
        'message': f'no need update',
        'git_version': device.version.git_version,
    }
    return JsonResponse(response_dict)

#成功update回報
def success_update(request, uid, git_version):
    if not Version.objects.filter(git_version=git_version).exists():
        return JsonResponse({'message', f'git_version {git_version} not found'})
    if not Device.objects.filter(uid=uid).exists():
        return JsonResponse({'message', f'device uid {uid} not found'})

    device = Device.objects.filter(uid=uid)[0]
    version = Version.objects.filter(git_version=git_version)[0]
    if not VersionLog.objects.filter(device=device, version=version).exists():
        VersionLog.objects.create(device=device, version=version)
    Device.objects.filter(uid=uid).update(version=version, 
                                          update_to_version=version)
    response_dict = {
        'message': f'success git_version {git_version} update to device {uid}'
    }
    return JsonResponse(response_dict)

#判斷alive
def alive_hook(devices, previous_check):
    device = devices[0]
    previous_check = previous_check # device.latest_check 
    time.sleep(15)
    if device.latest_check <= previous_check:
        devices.update(alive=False)
    return 

def i_am_alive(request, uid):
    devices = Device.objects.filter(uid=uid)
    devices.update(latest_check=datetime.now(), alive=True)
    latest_check = devices[0].latest_check 
    ps = Process(target=alive_hook, args=(devices, latest_check))
    ps.start()
    return JsonResponse({'message': 'ok got it'})

import time 
import os
import cv2
import numpy as np
from PIL import Image 
from django.core.files.base import ContentFile

def ring_image(request, uid):
    if request.method == "POST":
        # new image
        img_str = request.FILES['img'].read()
        nparr = np.fromstring(img_str, np.uint8)
        img_new = cv2.imdecode(nparr,  cv2.IMREAD_COLOR)
        cv2.imwrite(f"/home/iot/Desktop/iot_project/p2/server/tmp/{uid}/image.jpg", img_new)
        # old image
        try:
            img_old = cv2.imread(f"/home/iot/Desktop/iot_project/p2/server/tmp/{uid}/image.jpg")
        except:
            return HttpResponse("Good job first")
        # abnormal detection
        delta = np.mean( np.abs(img_new - img_old) )
        print(delta)
        if delta > 200:
            # Cool Down
            with open(f'/home/iot/Desktop/iot_project/p2/server/tmp/{uid}/abnormal_time.txt', 'r+') as f:
                value = float(f.read())
                f.seek(0)
                f.write(str(time.time()))
                f.truncate()
            if time.time()-value < 3:
                return HttpResponse("Good")
            
            frame_jpg = cv2.imencode('.jpg', np.asarray(img_new))
            file = ContentFile(frame_jpg[1])
            ab_image = Abnormal_Image()
            ab_image.image.save(str(np.random.randint(0,999999,1)[0])+".jpg", 
                                File(file), save=True)
            ab_image.save()
    return HttpResponse("GOOD Job !!")

video_page_url = ""
def get_video_page_url(request, uid):
    if request.method == "POST":
        data = request.POST 
        video_page_url = data['video_page_url']+"/index.html"
        f = open(f'/home/iot/Desktop/iot_project/p2/server/tmp/{uid}/video_page_url.txt', 'w')
        f.write(str(video_page_url))
        f.close()
        print(video_page_url)
    return HttpResponse("GOOD Job !!")

def ring_reply(request, uid):
    if request.method == "GET":
        value = 0
        '''
        with open(f'/home/iot/Desktop/iot_project/p2/server/tmp/{uid}/unlock.txt', 'r+') as f:
            value = f.read()
            f.seek(0)
            f.write(str(0))
            f.truncate()
        '''
        device = Device.objects.filter(uid=uid)[0]
        if Unlock.objects.filter(device=device).exists():
            value = 1
            Unlock.objects.filter(device=device).delete()
        return HttpResponse(value)

def ring_anomaly(request, uid):
    if request.method == "GET":
        # inform user and decide if close the door
        with open(f"/home/iot/Desktop/iot_project/p2/server/tmp/{uid}/anomaly.txt", 'w') as f:
            f.write(str(1))
    return HttpResponse("Receive Anomaly Door Open")

def have_anomaly(request, uid):
    value = "0"
    if not os.path.isfile(f"/home/iot/Desktop/iot_project/p2/server/tmp/{uid}/anomaly.txt"):
        return HttpResponse(value)
    if request.method == "GET":
        with open(f"/home/iot/Desktop/iot_project/p2/server/tmp/{uid}/anomaly.txt", 'r') as f:
            value = f.read()
    return HttpResponse(value)


def get_abnormal_time(request, uid, num):
    abnormal_images = Abnormal_Image.objects.all().order_by("timestamp").reverse()[:6]
    if 0 <= num and num < len(abnormal_images):
        return HttpResponse(str((abnormal_images[num].timestamp+timedelta(hours=8)).strftime("%Y-%m-%d-%H:%M:%S")))
    else:
        return HttpResponse("")

def get_abnormal_image(request, uid, num, time):
    abnormal_images = Abnormal_Image.objects.all().order_by("timestamp").reverse()[:6]
    if 0 <= num and num < len(abnormal_images):
        image_data = open(str(abnormal_images[num].image), "rb").read()
        print(abnormal_images[num].image)
        return HttpResponse(image_data,content_type="image/jpg")
    else:
        image_data = open('/home/iot/Desktop/iot_project/p2/server/media/loading.gif', 'rb').read()
        return HttpResponse(image_data,content_type="image/jpg")

def knock(request, uid):
    if request.method == "GET":
        '''
        # set knock
        with open(f'/home/iot/Desktop/iot_project/p2/server/tmp/{uid}/knock.txt', 'w') as f:
            f.write(str(1))
        # reset unlock
        with open(f'/home/iot/Desktop/iot_project/p2/server/tmp/{uid}/unlock.txt', 'w') as f:
            f.write(str(0))
        '''
        # set knock
        device = Device.objects.filter(uid=uid)[0]
        Knock.objects.create(device=device)
        if Unlock.objects.filter(device=device).exists():
            Unlock.objects.filter(device=device).delete()
    return HttpResponse("Good Job")

def have_knock(request, uid):
    value = 0
    if request.method == "GET":
        '''value = '0'
        if os.path.isfile(f'/home/iot/Desktop/iot_project/p2/server/tmp/{uid}/knock.txt'):
            with open(f'/home/iot/Desktop/iot_project/p2/server/tmp/{uid}/knock.txt', 'r') as f:
                value = f.read()
        '''
        device = Device.objects.filter(uid=uid)[0]
        if Knock.objects.filter(device=device).exists():
            value = 1
    return HttpResponse(str(value))

def unlock_page(request, uid):
    if request.method == "POST":
        '''
        set(uid, unlock=1, knock=0, anomaly=0)
        '''
        device = Device.objects.filter(uid=uid)[0]
        Unlock.objects.create(device=device)
        if Knock.objects.filter(device=device).exists():
            Knock.objects.filter(device=device).delete()
        return HttpResponse("Good Job Unlock door!!")
    video_page_url = "" 
    if os.path.isfile(f'/home/iot/Desktop/iot_project/p2/server/tmp/{uid}/video_page_url.txt'):
        f = open(f'/home/iot/Desktop/iot_project/p2/server/tmp/{uid}/video_page_url.txt', 'r')
        video_page_url = f.read()
        print(str(video_page_url))
    return render(request, 'ring/unlock.html', 
           {'current_time': str(datetime.now()), 
            'video_page_url': str(video_page_url),
            'uid': uid})

def logout(request):
    sessionid = request.COOKIES['csrftoken']
    Cookie.objects.filter(sessionid=sessionid).delete()
    return redirect('/ring/login')

def is_login(request):
    print(request.COOKIES)
    sessionid = request.COOKIES['csrftoken']
    if not Cookie.objects.filter(sessionid=sessionid).exists():
        return False
    cookies = Cookie.objects.filter(sessionid=sessionid)
    if timezone.make_aware(datetime.now() - timedelta(minutes=5), 
                            timezone.get_default_timezone()) > cookies[0].last_login:
        return False
    cookies.update(last_login=datetime.now())
    return True

def login(request):
    if is_login(request):
        return redirect('/ring/device_list')
    if request.method == "POST":
        #print(request.COOKIES)
        #print(request.COOKIES['sessionid'])
        #print(request.POST)
        uname = request.POST['uname']
        passwd = request.POST['psw']
        if not User.objects.filter(name=uname, passwd=passwd).exists():
            return redirect('/ring/login')
        #print(request.COOKIES)
        sessionid = request.COOKIES['csrftoken']
        Cookie.objects.create(sessionid=sessionid) 
        return redirect('/ring/device_list')
    return render(request, 'ring/login.html', {})

def device_list(request):
    if not is_login(request):
        redirect('/ring/login')
    devices = Device.objects.all().order_by('-latest_check')
    return render(request, 'ring/device_list.html',
            {'devices': devices})

def lock(request, uid):
    if request.method == "GET":
        '''
        set(uid, unlock=0, knock=0, anomaly=0)
        '''
        device = Device.objects.filter(uid=uid)[0]
        if Unlock.objects.filter(device=device).exists():
            Unlock.objects.filter(device=device).delete()
        if Knock.objects.filter(device=device).exists():
            Knock.objects.filter(device=device).delete()
    return HttpResponse("Lock")

def set(uid, unlock, knock, anomaly=0):
    # unlock door
    print("unlock click")
    with open(f'/home/iot/Desktop/iot_project/p2/server/tmp/{uid}/unlock.txt', 'w') as f:
       f.write(str(unlock))
    # reset have knock
    with open(f'/home/iot/Desktop/iot_project/p2/server/tmp/{uid}/knock.txt', 'w') as f:
       f.write(str(knock))
    # reset anomaly
    with open(f'/home/iot/Desktop/iot_project/p2/server/tmp/{uid}/anomaly.txt', 'w') as f:
       f.write(str(anomaly))
