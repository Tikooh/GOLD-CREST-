import matplotlib.pyplot as plt
import numpy as np
import torch

#model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

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
    plt.rcParams["figure.figsize"] = [500, 500] #defines matplotlib figure size
    plt.rcParams["figure.autolayout"] = True

    im = "mouse.jpg"

    # Inference
    results = model(im)

    # Results
    results.print()  # or .show(), .save(), .crop(), .pandas(), etc.

    results.xyxy[0]  # im predictions (tensor)
    initialCoords = results.pandas().xyxy[0]  # im predictions (pandas)

    x_centre = (initialCoords['xmin'][0] + initialCoords['xmax'][0]) / 2
    x_centre = x_centre.astype(int)
    y_centre = (initialCoords['ymin'][0] + initialCoords['ymax'][0]) / 2
    y_centre = y_centre.astype(int)   
    x_centre = np.array([x_centre])
    y_centre = np.array([y_centre])

    drone = drone(x_centre, y_centre)

    coords =[]
        
    #plot the points on the graph

    print(f"y = {drone.y} x = {drone.x}")
    plt.plot(drone.x, drone.y, 'r*')

    #zip the x and y coordinates into a tuple
    for xy in zip(drone.x, drone.y):
        coords.append(xy)
        plt.annotate(f'drone 1', xy=xy)
    
    plt.show()

    # linesegments(coords)
    # ang3Points(coords)
    






    # locationList = [drone(np.random.rand(1), np.random.rand(1)) for i in range(5)] #random locations

    # coords =[]
    # for index, i in enumerate(locationList):
        
    #     #plot the points on the graph
    #     plt.plot(i.x, i.y, 'r*')
    #     #zip the x and y coordinates into a tuple
    #     for xy in zip(i.x, i.y):
    #         coords.append(xy)
    #         plt.annotate(f'drone {index}', xy=xy)

    # linesegments(coords)
    # ang3Points(coords)