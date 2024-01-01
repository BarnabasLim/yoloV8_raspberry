import sys
import io
import PIL.Image as Image
def write_binary_to_jpg(file_path,content):
    try:
        write_path=file_path.replace("captured_vehicle/", "/home/barns/Desktop/")
        with open(write_path,'wb') as file:
            content=eval(content)
            file.write(content)
        print(f"jpg success")
    except  Exception as e:
        print("Error writing jpg :",e)
n=0
while True:
    user_in=input()
    if user_in:
        print(f"{n} line Barn: {user_in}")
        if user_in.startswith("image_file: "):
            file_path=user_in.replace("image_file: ","")
            content=input()
            if content:
                write_binary_to_jpg(file_path, content)
        n=n+1
