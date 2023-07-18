# import subprocess

# cmd = "python3 detect.py --weights '/Users/nanimuwu/Library/CloudStorage/OneDrive-AltrinchamGrammarSchoolforBoys/Sixth Form/Year 12/Gold Crest/yolov5-master/weights/best.pt' --source 0"

# p = subprocess.Popen(cmd, shell = True)
import torch
import time
import cv2
from PIL import Image
import numpy as np
import pathlib
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

gen_path = pathlib.Path.cwd()

DEVICE = "cuda" if torch.cuda.is_available() else "cpu" 

model = torch.hub.load('ultralytics/yolov5', 'custom', '/Users/nanimuwu/Library/CloudStorage/OneDrive-AltrinchamGrammarSchoolforBoys/Sixth Form/Year 12/Gold Crest/yolov5-master/weights/best.pt')

# im = 'https://www.trustedreviews.com/wp-content/uploads/sites/54/2022/05/dji-mini-3-pro-flight-2-920x518.jpg'
cam = cv2.VideoCapture(0)

while True:
    t1 = time.time()
    ret, frame = cam.read()
    frame = frame[:, :, [2,1,0]]
    frame = Image.fromarray(frame) 
    frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)

    result = model(frame,size=640)
    print(result.pandas().xyxy[0])
    cv2.imshow('YOLO', np.squeeze(result.render()))

    t2 = time.time()
    frq = 1/(t2-t1)
    print(f"fps:{frq}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
cam.release()
cv2.destroyAllWindows()