from edgetpumodel import EdgeTPUModel
from prediction import predictor
from prediction import drone
from utils import get_image_tensor

import cv2
import yaml
import os
import sys
import time
import pandas
import numpy as np

if __name__ == "__main__":
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
                
                else:
                    locationList = predictor.getLocationList(xlist, ylist, tlist)
                    predX, predY, predT = predictor.getPredictions(locationList)
                    predictor.tlist = predictor.tlist[:-1]
                    predictor.xlist = predictor.xlist[:-1]
                    predictor.ylist = predictor.ylist[:-1]
                    
        except KeyboardInterrupt:
            break

        cam.release()

            # ret,frame = im.read()
            # # print(f"ret output: {ret}, frame output: {frame}")

            # if ret:
            #     results = model(frame)
            #     # Results
            #     results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
            #     try:
                    
            #         for i in range(len(results)):
            #             results.xyxy[i]  # im predictions (tensor)
            #             initialCoords = results.pandas().xyxy[i]  # im predictions (pandas)
                        
            #             x_centre = np.array([(initialCoords['xmin'][0] + initialCoords['xmax'][0]) / 2])
            #             y_centre = np.array([(initialCoords['ymin'][0] + initialCoords['ymax'][0]) / 2])

            #             locationList.append(drone(x_centre, y_centre))
            #     except:
            #         print("Error")
                    
            #     cv2.imwrite(f"image{currentframe}.png",frame) #creates the image
            #     draw(f"image{currentframe}.png",initialCoords) #draws the box
            #     currentframe += 1