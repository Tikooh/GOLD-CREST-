import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import torch

class drone:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def linesegments(coords):
    lines = []
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

if __name__ == "__main__":
    #model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    matplotlib.use('TkAgg')
    im = ("drone1.png", "drone2.png", "drone3.jpg", "drone4.jpeg")

    # Inference
    results = model(im)
    # Results
    results.print()  # or .show(), .save(), .crop(), .pandas(), etc.

    locationList = []

    for i in range(len(results)):
        results.xyxy[i]  # im predictions (tensor)
        initialCoords = results.pandas().xyxy[i]  # im predictions (pandas)
        print(initialCoords)

        x_centre = np.array([(initialCoords['xmin'][0] + initialCoords['xmax'][0]) / 2])
        y_centre = np.array([(initialCoords['ymin'][0] + initialCoords['ymax'][0]) / 2])
        print(type(x_centre))

        locationList.append(drone(x_centre, y_centre))

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
            plt.annotate(f'drone {index}', xy=xy)

    
    linesegments(coords)
    ang3Points(coords)
    plt.show()