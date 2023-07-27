import matplotlib.pyplot as plt
import numpy as np
import pickle
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

    
    def predict(self, drone1: object, drone2, drone3, reqtime: float) -> np.ndarray:

        DIST = 50
        ttime = drone3.time-drone1.time

        distD1_D2 = drone2.coords - drone1.coords
        timeD1_D2 = drone2.time - drone1.time

        distD2_D3 = drone3.coords - drone2.coords
        timeD2_D3 = drone3.time - drone2.time

           #x                y                              x                 
        if distD1_D2[0]**2 + distD1_D2[1]**2 <= DIST**2 and distD2_D3[0]**2 + distD2_D3[1]**2 <= DIST**2:

            vf = distD1_D2*timeD1_D2/ttime+distD2_D3*timeD2_D3/ttime

            final = list(vf*reqtime + drone3.coords)
            
            # final[0] returns x coordinate, final[1] returns y
            return final[0],final[1],drone3.time+reqtime
        else:
            return None,None,None
    
    def getPredictions(self, locationList: list) -> list: 
        predX, predY, predT = [], [], []
        for i in range(len(locationList)-3):
            x,y,time = self.predict(locationList[i],locationList[i+1],locationList[i+2],1)

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
    # x = predictor.predict(locationList[150], locationList[151], locationList[152], 1)
    predX, predY, predT = predictor.getPredictions(locationList)
    predictor.plotGraph(predX, predY, predT)
    plt.show()