from picamera.array import PiRGBArray
from adafruit_motorkit import MotorKit
import RPi.GPIO as GPIO
from picamera import PiCamera
import time
import cv2
import numpy as np
import math

# Define GPIO to use on Pi
GPIO_SIG = 18  #Physical 12
CONTROL_PIN = 17 #Physical 11
PWM_FREQ = 50
STEP = 15

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PIN, GPIO.OUT)

pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
pwm.start(0)

kit = MotorKit()

def measurementInCM():
	
    chance = 5
	# setup the GPIO_SIG as output
    GPIO.setup(GPIO_SIG, GPIO.OUT)
	
    GPIO.output(GPIO_SIG, GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(GPIO_SIG, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(GPIO_SIG, GPIO.LOW)
    start = time.time()

    # setup GPIO_SIG as input
    GPIO.setup(GPIO_SIG, GPIO.IN)

    # get duration from Ultrasonic SIG pin
    while chance and GPIO.input(GPIO_SIG) == 0:
        start = time.time()
        # chance -= 1
	
    if not chance:
        print("No detected Signal\r")
        return 10000

    while GPIO.input(GPIO_SIG) == 1:
        stop = time.time()

    return measurementPulse(start, stop)


def measurementPulse(start, stop):
    # Calculate pulse length
    elapsed = stop-start

    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34300

    # That was the distance there and back so halve the value
    distance = distance / 2

    print(f"Distance : {distance:.1f} CM\r")
    return distance


def stop_secs(sec):
    kit.motor1.throttle = 0
    time.sleep(sec)

def forward(sec=1.0, power=0.5):
    kit.motor1.throttle = power 
    time.sleep(sec)
    stop_secs(0.1)

def backward(sec=1.0, power=0.5):
    kit.motor1.throttle = -1 * power
    time.sleep(sec)
    stop_secs(0.1)

def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return duty_cycle

def wheel(angle):
    for i in range(5):
        dc = angle_to_duty_cycle(angle)
        pwm.ChangeDutyCycle(dc)
        time.sleep(0.1)
    pwm.start(0)

angle=0 #全左轉
angle=48 #直行
angle=90 #全右轉

def left(angle=0):
    wheel(angle)	

def straight(angle=57):
    wheel(angle)

def right(angle=80):
    wheel(angle)

theta = 0
minLineLength = 20
maxLineGap = 10
with PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.framerate = 3
    rawCapture = PiRGBArray(camera, size=(320, 240))
    writer = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 1, (320,240))
    camera.start_preview()
    try:
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):  
            image = frame.array
            rawCapture.truncate(0)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edged = cv2.Canny(blurred, 85, 160)
            lines = cv2.HoughLinesP(edged,1,np.pi/180,10,minLineLength,maxLineGap)
            if ( lines is not None ):
                for x in range(0, len(lines)):
                    for x1,y1,x2,y2 in lines[x]:
                        cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
                        theta = theta + math.atan2((y2-y1),(x2-x1))
           #print(theta)GPIO pins were connected to arduino for servo steering control
            threshold = 3
            text = ""
            print(f'Theta {theta:.3f}', end='\r')
            #  print('Angle', theta * (180/math.pi))
            if measurementInCM() <= 15:
                text = "obstacle"
            elif ( theta > threshold ):
                if ( theta > 5):
                    left()
                    forward(0.1,0.65) #0.2,0.6
                else:
                    left()
                    forward(0.2,0.6) #0.2,0.6
                text = "left"
            elif ( theta < -threshold ):
                if ( theta < -5):
                    right()
                    forward(0.1,0.65) #0.2,0.6
                else:
                    right()
                    forward(0.2,0.6) #0.2,0.6
                text = "right"
            else:
                if (lines is None):
                    straight()
                    forward(0.3)
                    text = "straight"
                else:
                    straight()
                    forward(0.1)
                    text = "straight"
            theta = 0
            try:
                print(text, end='\r')
                if (text == "obstacle"):
                    d = ": " + measurementInCM() + " cm"
                    text += d
                    cv2.putText(image,text, (100,220), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
                    writer.write(image)
                    break
                cv2.putText(image,text, (100,220), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
                writer.write(image)
            except:
                break
    finally:
        stop_secs(0.1)
        camera.stop_preview()
        writer.release()
        
# Reset GPIO settings
GPIO.cleanup()
