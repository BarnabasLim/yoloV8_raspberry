from utils.utils import detect_count
from service.dataController import DataController
from picamera2 import Picamera2
from ultralytics import YOLO

import numpy as np
import cv2

import argparse

ap = argparse.ArgumentParser()

ap.add_argument("-t", "--telegram",action="store_true", 
help="send results to telegram")
ap.add_argument("-w", "--wifibroadcast", action="store_true",
help="send results through wifibroadast")
ap.add_argument("-d", "--debug", action="store_true",
help="activate debug mode")

args=vars(ap.parse_args())

#Start Camera
picam2=Picamera2()
picam2.start()

#Load Model
model= YOLO('yolov8n.pt')

debug_mode=args.get("debug", True)
print("debug_mode", debug_mode)

dataController=None

while True:
    img=picam2.capture_array("main")
    img=cv2.cvtColor(img,cv2.COLOR_RGBA2RGB)
    
    if debug_mode:
        print("Check img shape: ", np.array(img).shape,
            "n Check max: ", np.array(img).max())
    results=model.predict(source=img)
    detected_item=detect_count(results, debug_mode)
    im=results[0].plot()
    im=np.array(im)/255
    
    if debug_mode:
        cv2.imshow("Check this out", im)
    if dataController==None:
        del dataController
        dataController=None
        dataController=DataController(True, False, True)
    else:
        dataController.step(detected_item, img=im)
    
    if(cv2.waitKey(25) & 0xFF == ord("q")):
        if(dataController!=None):
            del dataController
        cv2.destroyAllWindows()
        break
    
