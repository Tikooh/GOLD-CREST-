from edgetpumodel import EdgeTPUModel
from prediction import Prediction, drone
from utils import get_image_tensor
import threading
import concurrent.futures
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

import cv2
import yaml
import os
import sys
import time
import pandas
import math
import numpy as np

def rotate(speed):# True=Clockwise, False=Counter-Clockwise, axis=0 for y, 1 for x
    with concurrent.futures.ThreadPoolExecutor() as executor:
        if LEFT:
            executor.submit(motors[1].motor_go, False, SPEEDS[speed] , 2, .0005, False)
        elif RIGHT:
            executor.submit(motors[1].motor_go, True, SPEEDS[speed] , 2, .0005, False)
        if UP:
            executor.submit(motors[0].motor_go, False, SPEEDS[speed] , 2, .0005, False)
        elif DOWN:
            executor.submit(motors[0].motor_go, True, SPEEDS[speed] , 2, .0005, False)

if __name__ == "__main__":

    direction = [22, 17]
    step = [23, 18]
    en = [24, 27]
    msx = [(26, 21, 20), (16, 19, 13)]

    motors = [RpiMotorLib.A4988Nema(direction[i], step[i], msx[i], "DRV8825") for i in range(2)]

    GPIO.setup(en[0],GPIO.OUT)
    GPIO.setup(en[1],GPIO.OUT)
    GPIO.output(en[0],GPIO.LOW)
    GPIO.output(en[1],GPIO.LOW)

    LEFT, RIGHT, UP, DOWN = False, False, False, False
    SPEEDS = ["Full", "Half", "1/4", "1/8", "1/16", "1/32"]

    model = EdgeTPUModel("Edge TPU/n640_edgetpu.tflite", "data.yaml")
    location_pred = Prediction()
    input_size = model.get_image_size()
    x = (255*np.random.random((3,*input_size))).astype(np.uint8)
    model.forward(x)
    
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FPS, 30)
    cam.set(3, 640)
    cam.set(4, 640)
    #cam.set(cv2.CAP_PROP_FPS, 30)
    currentFrame = 0
    while True:
        
        try:
            res, image = cam.read()
            image = cv2.rotate(image, cv2.ROTATE_180)
            if res is False:
                break

            else:
                full_image, net_image, pad = get_image_tensor(image, input_size[0])
                pred = model.forward(net_image)

                result = model.process_predictions(pred[0], full_image, pad, draw_img=True)

                tinference, tnms = model.get_last_inference_time()
                if result.size > 0:
                    x_centre = np.array([(result[0][0] + result[0][2]) / 2])
                    y_centre = np.array([(result[0][1] + result[0][3]) / 2])
                    location_pred.tlist.append(currentFrame)
                    location_pred.xlist.append(x_centre)
                    location_pred.ylist.append(y_centre)
                currentFrame += 1
                
                if len(location_pred.tlist) >= 3:
                    #TODO add motor controls
                    #locationList = location_pred.getLocationList(location_pred.xlist, location_pred.ylist, location_pred.tlist)
                    locationList = location_pred.getLocationList()
                    predX, predY, predT = location_pred.getPredictions(locationList) #each returns a list of size 1
                    location_pred.tlist = location_pred.tlist[-3:]
                    location_pred.xlist = location_pred.xlist[-3:]
                    location_pred.ylist = location_pred.ylist[-3:]
                    print(image.shape)
                    print(predX)
                    print(predY)
                    if (image.shape[1]/2)-predX[0] != 0 and (image.shape[0]/2)-predY[0] != 0:
                        speedX = math.floor(6*(1-(abs((image.shape[1]/2)-predX[0])/image.shape[1]/2)))
                        speedY = math.floor(6*(1-(abs((image.shape[0]/2)-predY[0])/image.shape[0]/2)))

                    if predX[0] < image.shape[1]/2:
                        LEFT = True
                        RIGHT = False
                        DOWN = False
                        UP = False
                        rotate(speedX)
                    else:
                        LEFT = False
                        RIGHT = True
                        DOWN = False
                        UP = False
                        rotate(speedX)

                    if predY[0] < image.shape[0]/2:
                        LEFT = False
                        RIGHT = False
                        DOWN = False
                        UP = True
                        rotate(speedY)
                    else:
                        LEFT = False
                        RIGHT = False
                        DOWN = True
                        UP = False
                        rotate(speedY)
                        
        except KeyboardInterrupt:
            break

    cam.release()