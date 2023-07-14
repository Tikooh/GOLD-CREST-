import random
import matplotlib.pyplot as plt
import math

class droneimage:
    def __init__(self,x,y,time):
        self.x =x
        self.y =y
        self.time = time
        
    def display(self):
        print(f"Coords are ({self.x},{self.y}), picture taken at time {self.time}")  
        
images = [droneimage(random.randint(1,50),random.randint(1,50),random.randint(100,2000)) for x in range(10)]
# coords = [(0,0),(0,1),(1,1),(1,0),(0,0)]
# coords = [(1,1),(2,2),(3,1),(2,0),(1,1)]
# coords = [(1,1),(2,3),(4,2),(3,0),(1,1)]
# coords = [(1,0),(0,1),(0,2),(1,3),(2,3),(3,2),(3,1),(2,0),(1,0)]
# images = [droneimage(coords[x][0],coords[x][1],0) for x in range(len(coords))]
images.sort(key=lambda x:x.time)
# for image in images:
#     image.display()

    
def gb(x1,y1,x2,y2):
    dy,dx = y2-y1,x2-x1
    h = math.sqrt(dx**2+dy**2)+0.00001
    offset = 0
    if dx*dy>=0:
        sin = dx/h if dx>=0 else -dx/h
    else:
        sin = dy/h if dy>=0 else -dy/h
    if dx>0 and dy>0:
        offset = 0
    elif dx>0 and dy<0:
        offset = 90
    elif dx<=0 and dy<=0:
        offset = 180
    elif dx<0 and dy>0:
        offset = 270
    angle = math.asin(sin)*180/math.pi
    # return angle,angle+offset
    return str(round(angle+offset,2))
    

def speed(img1,img2):
    dy,dx,dt = img2.y-img1.y,img2.x-img1.x,img2.time-img1.time
    h = math.sqrt(dx**2+dy**2)
    speed = h/(dt+0.00001)
    return str(round(speed,2))
    
    

for i in range(len(images)-1):
    print(f"Drone travelling on bearing {gb(images[i].x,images[i].y,images[i+1].x,images[i+1].y)} with speed of {speed(images[i],images[i+1])} units, from {(images[i].x,images[i].y)} to {(images[i+1].x,images[i+1].y)}")

#plotting
xlist = [images[x].x for x in range(len(images))]
ylist = [images[x].y for x in range(len(images))]
tlist = [images[x].time for x in range(len(images))]



plt.plot()
plt.title("test")
plt.scatter(xlist,ylist)
plt.plot(xlist,ylist)
plt.xlim(0,50)
plt.ylim(0,50)
for x,y in zip(xlist,ylist):

    label = f"({x},{y})"

    plt.annotate(label,(x,y),textcoords="offset points",xytext=(0,10),ha='center') 
plt.show()