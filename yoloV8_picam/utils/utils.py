
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
