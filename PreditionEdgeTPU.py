from edgetpumodel import EdgeTPUModel
from prediction import predictor
from prediction import drone
from utils import get_image_tensor
import threading
import concurrent.futures
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
from Controller import increase_speed, decrease_speed, rotate

import cv2
import yaml
import os
import sys
import time
import pandas
import numpy as np

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
    SPEED = 4
    SPEEDS = ["Full", "Half", "1/4", "1/8", "1/16", "1/32"]

    model = EdgeTPUModel()
    location_pred = predictor([],[],[])
    input_size = model.get_image_size()
    
    cam = cv2.VideoCapture(0)
    currentFrame = 0
    while True:
        
        try:
            res, image = cam.read()

            if res is False:
                break

            else:
                tlist, xlist, ylist = [],[],[]

                if len(tlist) <= 2:

                    full_image, net_image, pad = get_image_tensor(image, input_size[0])
                    pred = model.forward(net_image)

                    result = model.process_predictions(pred[0], full_image, pad)

                    tinference, tnms = model.get_last_inference_time()

                    result = result.pandas()
                    x_centre = np.array([(result['xmin'][0] + result['xmax'][0]) / 2])
                    y_centre = np.array([(result['ymin'][0] + result['ymax'][0]) / 2])

                    predictor.tlist.append(currentFrame)
                    predictor.xlist.append(x_centre)
                    predictor.ylist.append(y_centre)
                    currentFrame += 1

                    if x_centre

                    rotate()
                
                else:
                    #TODO add motor controls
                    locationList = predictor.getLocationList(xlist, ylist, tlist)
                    predX, predY, predT = predictor.getPredictions(locationList)
                    predictor.tlist = predictor.tlist[:-1]
                    predictor.xlist = predictor.xlist[:-1]
                    predictor.ylist = predictor.ylist[:-1]

                    rotate()
        except KeyboardInterrupt:
            break

        cam.release()