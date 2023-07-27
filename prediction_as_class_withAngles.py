import matplotlib.pyplot as plt
import numpy as np
import pickle
import math
WRITE = False
class drone:
    def __init__(self, x: float, y: float, time: float) -> None:
        self._coords = np.array([x, y])
        self.time = time
    
    @property
    def coords(self) -> np.ndarray:
        return self._coords
    @coords.setter
    def coords(self, value) -> None:
        try:
            type(value) == tuple
            self._coords = np.array(value)
        except:
            raise TypeError("Incorrect type: Must be Tuple")

class Prediction:
    def __init__(self) -> None:
        self.xlist = list(filter(lambda x: x>0, self.read_list("xlist")))
        self.ylist = list(filter(lambda x: x>0, self.read_list("ylist")))
        self.tlist = self.read_list("tlist")

    @staticmethod
    def read_list(name) -> list:
        with open(f'{name}', 'rb') as fp:
            n_list = pickle.load(fp)
            return n_list
    
    def getLocationList(self) -> list:
        return [drone(self.xlist[i],self.ylist[i],self.tlist[i]) for i in range(len(self.xlist))]

    
    def predict(self, drone1: object, drone2, drone3, drone4, drone5, reqtime: float) -> np.ndarray:

        DIST = 50
        ttime = drone3.time-drone1.time
        ang1 = 1000
        ang2 = 100
        ang3 = 100000
        print(drone1.coords[0])
        print(drone2.coords[0])
        if (drone1.coords[0] < drone2.coords[0] and drone2.coords[0] < drone3.coords[0]) or (drone1.coords[0] > drone2.coords[0] and drone2.coords[0] > drone3.coords[0]):
            ang1 = self.calculateAngle(drone1.coords, drone2.coords, drone3.coords)
            ang2 = self.calculateAngle(drone2.coords, drone3.coords, drone4.coords)
            ang3 = self.calculateAngle(drone3.coords, drone4.coords, drone5.coords)

            print(f"ang1 {ang1} ang2 {ang2} ang3 {ang3}")
        distD3_D4 = drone4.coords - drone3.coords
        timeD3_D4 = drone4.time - drone3.time

        distD4_D5 = drone5.coords - drone4.coords
        timeD4_D5 = drone5.time - drone4.time

           #x                y                              x                 
        if distD3_D4[0]**2 + distD3_D4[1]**2 <= DIST**2 and distD4_D5[0]**2 + distD4_D5[1]**2 <= DIST**2:

            vf = distD3_D4*timeD3_D4/ttime+distD4_D5*timeD4_D5/ttime

            final = list(vf*reqtime + drone5.coords)

            if (abs(ang1-ang2) < 15) and (abs(ang2-ang3) < 15):
                print(f"ang1 {ang1}")
                ang = ((180-ang1) + (180-ang2) +(180-ang3)) /3
                if drone1.coords[0] > drone2.coords[0] and drone2.coords[0] > drone3.coords[0]:
                    ang = math.pi/180 * (360 - ang)
                else:
                    ang = math.pi/180*(ang)

                cartesianx = (final[0]*math.cos(ang)-final[1]*math.sin(ang))
                cartesiany = (final[0]*math.sin(ang)+final[1]*math.cos(ang))
                print(f"cartesianx {cartesianx} cartesiany {cartesiany}")
                # print(final[0], final[1])

                final[0] = cartesianx
                final[1] = cartesiany
                # radius = math.sqrt(final[0]**2 + final[1]**2)
                # print(radius)
                # length = math.sqrt(radius**2 + radius**2 - 2*(radius)*(radius)*(math.cos(math.pi/180 * (180-ang1))))
                # print(length)

            
            # final[0] returns x coordinate, final[1] returns y
            return final[0],final[1],drone5.time+reqtime
        else:
            return None,None,None
        
    def calculateAngle(self, D1, D2, D3):
            ba = np.ndarray.flatten(D1-D2)
            bc = np.ndarray.flatten(D3-D2)

            #dot product to work out the angle
            cosine_angle = np.dot(ba,bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            angle = float((np.arccos(cosine_angle)) * (180/np.pi))
            # print(f"Angle is {angle}")
            return angle
    
    def getPredictions(self, locationList: list) -> list: 
        predX, predY, predT = [], [], []
        for i in range(len(locationList)-5):
            x,y,time = self.predict(locationList[i],locationList[i+1],locationList[i+2], locationList[i+3], locationList[i+4],1)

            if x!= None:
                predX.append(x) 
                predY.append(y) 
                predT.append(time)
        return predX, predY, predT

    def plotGraph(self, predX: list, predY, predT) -> None:
        plt.plot()
        plt.scatter(self.xlist, self.ylist)
        plt.plot(self.xlist, self.ylist)
        for x,y,t in zip(self.xlist,self.ylist,self.tlist):
            label = f"drone {t}"
            plt.annotate(label,(x,y),textcoords="offset points",xytext=(0,10),ha='center')
        
        #prediction points
        plt.scatter(predX,predY)
        plt.plot(predX,predY)
        for x1,y1,t1 in zip(predX,predY,predT):
            label = f"prediction {t1}"
            plt.annotate(label,(x1,y1),textcoords="offset points",xytext=(0,10),ha='center')


# def write_list(a_list,name):
#     with open(f'{name}', 'wb') as fp:
#         pickle.dump(a_list, fp)
#         print('Done writing list into a binary file'

if __name__ == "__main__":
    predictor = Prediction()
    locationList = predictor.getLocationList()
    x = predictor.predict(locationList[630], locationList[631], locationList[632], locationList[633], locationList[634], 1)
    print(locationList[635].coords[0])
    predX, predY, predT = predictor.getPredictions(locationList)
    predictor.plotGraph(predX, predY, predT)
    plt.show()