import json
import time
from subprocess import Popen, PIPE

# run rpi_camera_survellance_system.py
p0 = Popen(['python3', 'rpi_camera_surveillance_system.py'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
print("start camera success")

# run ngrok
p1 = Popen(['./ngrok','http','8000'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
print("run ngrok success")

# get public streaming url
get_success = False
while get_success==False:
    try:
        p2 = Popen(['curl','http://127.0.0.1:4040/api/tunnels'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
        output = p2.stdout.read()
        stream_public_url = json.loads(output.decode('utf-8'))["tunnels"][0]["public_url"]
        get_success = True
    except:
        time.sleep(0.2)
print(stream_public_url)

# send url to server
import requests
from datetime import datetime as dt

url = 'http://lab.wubinray.com:8000/ring/video_page_url/'
data = {'timestamp': dt.now().strftime("%m%d_%H%M%S"),
        'video_page_url': stream_public_url}
requests.post(url, data=data)
print(f"post video_page_public_url to {url}")

#input("stop")

#p0.kill()
#p1.kill()
#p2.kill()


