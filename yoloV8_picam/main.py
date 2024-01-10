from utils.utils import detect_count, motion_detection
from service.dataController import DataController
from picamera2 import Picamera2
from ultralytics import YOLO

import numpy as np
import cv2

import argparse
import time

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
picam2.preview_configuration.enable_lores()
picam2.configure("preview")
w,h = picam2.preview_configuration.lores.size
print("check", w, h, picam2.preview_configuration.lores.size)
picam2.start()

#Load Model
model= YOLO('yolov8n.pt')

debug_mode=args.get("debug", True)
print("debug_mode", debug_mode)

dataController=None

motion_detected=False
start_time=time.time()
curr_time=start_time
prev_time=curr_time
curr_img=picam2.capture_buffer("lores")
prev_img=curr_img

if(debug_mode):
    #for difference pic
    curr_img_main=picam2.capture_array("main")
    prev_img_main=curr_img_main

while True:
    
    if motion_detected:
        #motion_detected mode
        if curr_time-start_time<20:
            #20 sec object detection mode
            curr_time=time.time()
            
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
            if dataController==None or curr_time-prev_time>10:
                prev_time=time.time()
                if dataController:
                    dataController.step_end()
                del dataController
                dataController=None
                dataController=DataController(True, False, debug_mode)
            else:
                if dataController.step(detected_item, img=im):
                    start_time=time.time()
                    #curr_time=start_time
                    #prev_time=curr_time
                    
        else:
            #20 sec object detection mode end
            motion_detected=False
            
            if dataController:
                dataController.step_end()
            del dataController
            dataController=None
            dataController=DataController(True, False, debug_mode)
    else:
        #motion not detected mode
        curr_img=picam2.capture_buffer("lores")
        if(debug_mode):
            #for difference pic
            curr_img_main=picam2.capture_array("main")

        
        motion_detected=motion_detection(curr_img,prev_img,w, h,7,debug_mode)
        
        if(motion_detected):
            #First time motion detected
            start_time=time.time()
            curr_time=start_time
            prev_time=curr_time
            
            
            if dataController:
                dataController.step_end()
            del dataController
            dataController=None
            dataController=DataController(True, False, debug_mode)
            
            img=picam2.capture_array("main")
            img=cv2.cvtColor(img,cv2.COLOR_RGBA2RGB)
            img=img/255
            dataController.step_start(img)
            if(debug_mode):
                #for difference pic
                #print("Check curr_img_main shape: ", np.array(curr_img_main).shape)
                #print("Check prev_img_main shape: ", np.array(prev_img_main).shape)
                frame_delta=cv2.absdiff(prev_img_main,curr_img_main)
                frame_threshold=cv2.threshold(frame_delta,25, 255, cv2.THRESH_BINARY)[1]
                #print("Check frame_threshold shape: ", np.array(frame_threshold).shape)
                dataController.step_start(frame_threshold*255)
        else:
            time.sleep(1)
        prev_img=curr_img
        if(debug_mode):
            #for difference pic
            prev_img_main=curr_img_main
        
        
    if(cv2.waitKey(25) & 0xFF == ord("q")):
        if(dataController!=None):
            del dataController
        cv2.destroyAllWindows()
        break
    
