import cv2
from keras.models import model_from_json
import numpy as np
import libcamera
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import time
#import Picamera2
# from keras_preprocessing.image import load_img
json_file = open("emotiondetector.json", "r")
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)

model.load_weights("emotiondetector.h5")
haar_file=cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade=cv2.CascadeClassifier(haar_file)
cv2.startWindowThread()

red_pin=26
green_pin=27
blue_pin=17

GPIO.setmode(GPIO.BCM)
GPIO.setup(red_pin,GPIO.OUT, initial = 1)
GPIO.setup(green_pin,GPIO.OUT, initial = 1)
GPIO.setup(blue_pin,GPIO.OUT, initial = 1)

def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1,48,48,1)
    return feature/255.0
    
def red():
 GPIO.output(red_pin,GPIO.LOW)
 GPIO.output(green_pin,GPIO.HIGH)
 GPIO.output(blue_pin,GPIO.HIGH)
 
def turnoff():
    GPIO.output(red_pin,GPIO.HIGH)
    GPIO.output(green_pin,GPIO.HIGH)
    GPIO.output(blue_pin,GPIO.HIGH)
 

def yellow():
 GPIO.output(red_pin,GPIO.LOW)
 GPIO.output(green_pin,GPIO.LOW)
 GPIO.output(blue_pin,GPIO.HIGH)
 
def white():
    GPIO.output(red_pin,GPIO.LOW)
    GPIO.output(green_pin,GPIO.LOW)
    GPIO.output(blue_pin,GPIO.LOW)
    
def blue():
    GPIO.output(red_pin,GPIO.HIGH)
    GPIO.output(green_pin,GPIO.HIGH)
    GPIO.output(blue_pin,GPIO.LOW) 

camera = "/base/soc/i2c0mux/i2c@1/ov5647@36"
pipeline = "libcamerasrc camera-name=%s ! video/x-raw,width=640,height=480,framerate=10/1,format=RGBx ! videoconvert ! videoscale ! video/x-raw,width=640,height=480,format=BGR ! appsink" % (camera)
#webcam=cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888' , "size": (640,480)}))
picam2.start()
labels = {0 : 'angry', 1 : 'disgust', 2 : 'fear', 3 : 'happy', 4 : 'neutral', 5 : 'sad', 6 : 'surprise'}
while True:
    #if not webcam.isOpened():
    #    print("Camera not opened")
    #i,im=webcam.read()
    im = picam2.capture_array()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(im,1.3,5)
    try: 
        for (p,q,r,s) in faces:
            image = gray[q:q+s,p:p+r]
            cv2.rectangle(im,(p,q),(p+r,q+s),(255,0,0),2)
            image = cv2.resize(image,(48,48))
            img = extract_features(image)
            pred = model.predict(img)
            prediction_label = labels[pred.argmax()]
            print("Predicted Output:", prediction_label)
            f = open("emotiondata.txt", "w")
            f.write(prediction_label)
            #do if else for prediction label to change led light
            if prediction_label == 'happy':
                turnoff()
                yellow()
                time.sleep(1)
            elif prediction_label == 'sad' or prediction_label == 'fear':
                turnoff()
                blue()
                time.sleep(1)
            elif prediction_label == 'angry':
                turnoff()
                red()
                time.sleep(1)
            elif prediction_label == 'neutral':
                turnoff()
                white()
                time.sleep(1)
            else:
                turnoff()
                time.sleep(1)

            #   write code to light led to desired color
            #elif prediction_label == 'neutral':
            #   write code to light led to desired color
            #cv2.putText(im,prediction_label)
            cv2.putText(im, '% s' %(prediction_label), (p-10, q-10),cv2.FONT_HERSHEY_COMPLEX_SMALL,2, (0,0,255))
        cv2.imshow("Output",im)
        cv2.waitKey(27)
    except cv2.error:
        pass
    except KeyboardInterrupt:
                GPIO.cleanup()
