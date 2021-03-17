import os
import subprocess
import time
import serial
import requests
from datetime import datetime as dt

def send():
    #os.system("python3 run_ngrok.py")
    proc = subprocess.Popen(['python3', 'run_ngrok.py'])
    url = 'http://lab.wubinray.com:8000/ring/knock/'
    requests.get(url, timeout=5)

def send_anomaly():
    url = 'http://lab.wubinray.com:8000/ring/anomaly/'
    res = requests.get(url, timeout=5)
    reply = res.content.decode("utf-8")
    return reply

def wait():
    url = 'http://lab.wubinray.com:8000/ring/reply/'
    res = requests.get(url, timeout=5)
    reply = res.content.decode("utf-8")
    count = 0
    while (count < 10 and reply == "0"):
        time.sleep(3)
        count += 1
        res = requests.get(url, timeout=3)
        reply = res.content.decode("utf-8")
    if (reply  == "0"):
        print("Sorry, bye!")
        url = 'http://lab.wubinray.com:8000/ring/lock/'
        requests.get(url, timeout=5)
    elif (reply == "1"):
        print("Come in, baby!")
    return reply

def door_control(ser, reply):
    l = ""
    if reply == "0":
        ser.write(b"0")
        while not (l == "Close"):
            l = ser.readline().decode('utf-8').rstrip()
            time.sleep(1)
    elif reply == "1":
        ser.write(b"1")
        while not (l == "Open"):
            l = ser.readline().decode('utf-8').rstrip()
            time.sleep(1)
            # subprocess.Popen("pkill -f rpi_camera_surveillance_system.py", shell=True)
            # subprocess.Popen("pkill -f ngrok", shell=True)
    print(l)

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    # test
    send()
    print(wait())
    while True:
        l = ser.readline().decode('utf-8').rstrip()
        if l == "Knock":
            print("Knock")
            send()
            reply = wait()
            door_control(ser,reply)
        elif l == "Anomaly":
            #print("Anomaly")
            send_anomaly()
        
                
