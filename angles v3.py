import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import torch
import cv2

class drone:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def linesegments(coords):
    for i in range(len(coords)):
        try:
            #plot the line segments
            x_values = [coords[i][0], coords[i+1][0]] #
            y_values = [coords[i][1], coords[i+1][1]]
        except:
            print("Error: Reached final point")

        plt.plot(x_values, y_values, 'bo', linestyle="-")

def ang3Points(coords):
    for i in range(len(coords)):
        a = np.asarray(coords[i])
        try:
            b = np.asarray(coords[i+1])
            c = np.asarray(coords[i+2])
        except:
            print("Out of range")

        ba = a - b
        bc = c - b

        #dot product to work out the angle
        cosine_angle = np.dot(ba,bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = (np.arccos(cosine_angle)) * (180/np.pi)

        print(f"Angle: {angle}")

def draw(imagepath,coords): #imagepath is currently just the image name : will need to change this a bit if saving in another folder
    image = cv2.imread(imagepath)
    startpoint,endpoint = (round(coords['xmin'][0]),round(coords['ymax'][0])),(round(coords['xmax'][0]),round(coords['ymin'][0]))
    image = cv2.rectangle(image,startpoint,endpoint,(255,0,0),20)
    cv2.imwrite(imagepath,image)

def BBmodel(model):
    # Inference
    im = cv2.VideoCapture("VID_20230713_151704.mp4")

    currentframe = 0
    locationList = []
    while True:
                    # reading from frame
            ret,frame = im.read()
            # print(f"ret output: {ret}, frame output: {frame}")

            if ret:
                results = model(frame)
                # Results
                results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
                try:
                    
                    for i in range(len(results)):
                        results.xyxy[i]  # im predictions (tensor)
                        initialCoords = results.pandas().xyxy[i]  # im predictions (pandas)
                        
                        x_centre = np.array([(initialCoords['xmin'][0] + initialCoords['xmax'][0]) / 2])
                        y_centre = np.array([(initialCoords['ymin'][0] + initialCoords['ymax'][0]) / 2])

                        locationList.append(drone(x_centre, y_centre))
                except:
                    print("Error")
                currentframe += 1
                cv2.imwrite(f"image{currentframe}.png",frame) #creates the image
                draw(f"image{currentframe}.png",initialCoords) #draws the box
            else:
                break

    print(locationList)
    return locationList

if __name__ == "__main__":
    #model
    model = torch.hub.load('ultralytics/yolov5', 'custom', '/Users/Piotr/Documents/VS Code/crest/exp10-s.pt') 
    matplotlib.use('TkAgg') #change backend after loading model https://github.com/ultralytics/yolov5/issues/2779

    locationList = BBmodel(model)

    coords =[]
    # plt.rcParams["figure.figsize"] = [500, 500] #defines matplotlib figure size
    # plt.rcParams["figure.autolayout"] = True    
    for index, i in enumerate(locationList):
        
        #plot the points on the graph
        plt.plot(i.x, i.y, 'r*')
        print(i.x)
        #zip the x and y coordinates into a tuple
        for xy in zip(i.x, i.y):
            coords.append(xy)
            # plt.annotate(f'drone {index}', xy=xy)

    
    linesegments(coords)
    ang3Points(coords)
    plt.show()