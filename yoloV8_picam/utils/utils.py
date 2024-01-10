import numpy as np

def detect_count(results, debug_mode=False):
    detected_item={}
    class_id=results[0].boxes.cls.cpu().numpy().astype(int)
    names=results[0].names
    
    for i in class_id:
        if names[i] in detected_item:
            detected_item[names[i]]=detected_item[names[i]]+1
        else:
            detected_item[names[i]]=1
    if(debug_mode):
        print(detected_item)
    return detected_item
    
def cat(file_path):
    print(file_path)
    try: 
        with open(file_path,'rb') as file:
            content=file.read()
            print(f"image_file: {file_path}")
            print(content)
            print(type(content))
    except FileNotFoundError:
        print(f"File not found: {file_path}")

def motion_detection(curr, prev,w,h, threshold=7, debug=False):
    #Measure pixel differences between current and previous frames
    curr=curr[:w*h].reshape(h,w)
    prev=prev[:w*h].reshape(h,w)
    mse=np.square(np.subtract(curr,prev)).mean()
    if(debug):
        print("motion_detection", mse)
    if mse > threshold:
        return True
    else:
        return False
        
