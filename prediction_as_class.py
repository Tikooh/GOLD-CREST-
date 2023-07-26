import matplotlib.pyplot as plt
import numpy as np
import pickle
WRITE = False
class drone:
    def __init__(self, x: float, y: float, time: float) -> None:
        self.x = x
        self.y = y
        self.time = time

class Prediction:
    def __init__(self) -> None:
        self.xlist = list(filter(lambda x: x>0, self.read_list("xlist")))
        self.ylist = list(filter(lambda x: x>0, self.read_list("ylist")))
        self.tlist = self.read_list("tlist")
        self.DIST = 100

    @staticmethod
    def read_list(name) -> list:
        with open(f'{name}', 'rb') as fp:
            n_list = pickle.load(fp)
            return n_list
    
    def getLocationList(self) -> list:
        return [drone(self.xlist[i],self.ylist[i],self.tlist[i]) for i in range(len(self.xlist))]
    
    def predict(self, drone1: object, drone2, drone3, reqtime: float) -> np.ndarray:
        ttime = drone3.time-drone1.time
        v1,v2,v3 = np.array([drone1.x,drone1.y]),np.array([drone2.x,drone2.y]),np.array([drone3.x,drone3.y])
        if (v2-v1)[0]**2 + (v2-v1)[1]**2 <= self.DIST**2 and (v3-v2)[0]**2 + (v3-v2)[1]**2 <= self.DIST**2:
            vf = (v2-v1)*(drone2.time-drone1.time)/ttime+(v3-v2)*(drone3.time-drone2.time)/ttime
            final = list(vf*reqtime + v3)
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
    predX, predY, predT = predictor.getPredictions(locationList)
    predictor.plotGraph(predX, predY, predT)
    plt.show()