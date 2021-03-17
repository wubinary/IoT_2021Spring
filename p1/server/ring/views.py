from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.core.files import File 
from datetime import datetime, timedelta 
from .models import Abnormal_Image
import json

def index(request):
    return render(request, 'ring/index.html', {
        'current_time': str(datetime.now()),
    })

import time
import cv2
import numpy as np
from PIL import Image 
from django.core.files.base import ContentFile

def ring_image(request):
    if request.method == "POST":
        #print(request.POST)
        # old image
        img_old = cv2.imread("tmp/image.jpg")
        # new image
        img_str = request.FILES['img'].read()
        nparr = np.fromstring(img_str, np.uint8)
        img_new = cv2.imdecode(nparr,  cv2.IMREAD_COLOR)
        cv2.imwrite("tmp/image.jpg", img_new)
        # abnormal detection
        delta = np.mean( np.abs(img_new - img_old) )
        print(delta)
        if delta > 200:
            # Cool Down
            with open('tmp/abnormal_time.txt', 'r+') as f:
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
def get_video_page_url(request):
    if request.method == "POST":
        data = request.POST 
        video_page_url = data['video_page_url']+"/index.html"
        f = open('tmp/video_page_url.txt', 'w')
        f.write(str(video_page_url))
        f.close()
        print(video_page_url)
    return HttpResponse("GOOD Job !!")

def ring_reply(request):
    if request.method == "GET":
        value = 0
        with open('tmp/unlock.txt', 'r+') as f:
            value = f.read()
            f.seek(0)
            f.write(str(0))
            f.truncate()
        return HttpResponse(value)

def ring_anomaly(request):
    if request.method == "GET":
        # inform user and decide if close the door
        with open("tmp/anomaly.txt", 'w') as f:
            f.write(str(1))
    return HttpResponse("Receive Anomaly Door Open")

def have_anomaly(request):
    value = 0
    if request.method == "POST":
        with open("tmp/anomaly.txt", 'r') as f:
            value = f.read()
    return HttpResponse(value)


def get_abnormal_time(request, num):
    abnormal_images = Abnormal_Image.objects.all().order_by("timestamp").reverse()[:6]
    if 0 <= num and num < len(abnormal_images):
        return HttpResponse(str((abnormal_images[num].timestamp+timedelta(hours=8)).strftime("%Y-%m-%d-%H:%M:%S")))
    else:
        return HttpResponse("")

def get_abnormal_image(request, num, time):
    abnormal_images = Abnormal_Image.objects.all().order_by("timestamp").reverse()[:6]
    if 0 <= num and num < len(abnormal_images):
        image_data = open(str(abnormal_images[num].image), "rb").read()
        print(abnormal_images[num].image)
        return HttpResponse(image_data,content_type="image/jpg")
    else:
        image_data = open('media/loading.gif', 'rb').read()
        return HttpResponse(image_data,content_type="image/jpg")

def knock(request):
    if request.method == "GET":
        # set knock
        with open('tmp/knock.txt', 'w') as f:
            f.write(str(1))
        # reset unlock
        with open('tmp/unlock.txt', 'w') as f:
            f.write(str(0))
    return HttpResponse("Good Job")

def have_knock(request):
    value = 0
    if request.method == "POST":
        with open('tmp/knock.txt', 'r') as f:
            value = f.read()
    return HttpResponse(value)

def unlock_page(request):
    if request.method == "POST":
        set(unlock=1, knock=0, anomaly=0)
        return HttpResponse("Good Job Unlock door!!") 
    video_page_url = "" 
    f = open('tmp/video_page_url.txt', 'r')
    video_page_url = f.read()
    print(str(video_page_url))
    return render(request, 'ring/unlock.html', 
           {'current_time': str(datetime.now()), 
            'video_page_url': str(video_page_url)})

def lock(request):
    if request.method == "GET":
        set(unlock=0, knock=0, anomaly=0)
    return HttpResponse("Lock")

def set(unlock, knock, anomaly=0):
    # unlock door
    print("unlock click")
    with open('tmp/unlock.txt', 'w') as f:
       f.write(str(unlock))
    # reset have knock
    with open('tmp/knock.txt', 'w') as f:
       f.write(str(knock))
    # reset anomaly
    with open('tmp/anomaly.txt', 'w') as f:
       f.write(str(anomaly))
