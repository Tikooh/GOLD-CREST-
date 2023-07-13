import matplotlib.pyplot as plt
import numpy as np

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
    plt.rcParams["figure.figsize"] = [7.5, 3.5] #defines matplotlib figure size
    plt.rcParams["figure.autolayout"] = True

    locationList = [drone(np.random.rand(1), np.random.rand(1)) for i in range(5)] #random locations
    print(np.random.rand(1))
    print(type(np.random.rand(1)))
    coords =[]
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