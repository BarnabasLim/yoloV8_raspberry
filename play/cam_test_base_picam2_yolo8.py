from picamera2 import Picamera2
from ultralytics import YOLO

import numpy as np
import cv2

#Start Camera
picam2=Picamera2()
picam2.start()

#Load Model
model= YOLO('yolov8n.pt')

while True:
    img=picam2.capture_array("main")
    img=cv2.cvtColor(img,cv2.COLOR_RGBA2RGB)
    print("Check img shape: ", np.array(img).shape,
          "n Check max: ", np.array(img).max())
    results=model.predict(source=img)
    im=results[0].plot()
    im=np.array(im)/255
    cv2.imshow("Check this out", im)
    
    if(cv2.waitKey(25) & 0xFF == ord("q")):
        cv2.destroyAllWindows()
        break
    