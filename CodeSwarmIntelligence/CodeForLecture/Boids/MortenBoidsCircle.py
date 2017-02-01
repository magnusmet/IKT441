import random
import math

circlepoints = []
r = 50
cent = [50,50]
for i in range(10):
    angle = float(i)#float(random.uniform(i,100))#float(i)#/(math.pi)#random.random()*math.pi*r*2
    circlepoints.append((math.cos(angle)*r+cent[0], math.sin(angle)*r+cent[1])) 

def getDirection(boid):
    x,y = circlepoints[0]
    distance = abs(math.sqrt((boid.x-x)**2 + (boid.y-y)**2))
    smallestx,smallesty,smallestdistance,smallesti = x,y,distance,0
    i = 0
    for x,y in circlepoints:
        distance = abs(math.sqrt((boid.x-x)**2 + (boid.y-y)**2))
        if(distance<smallestdistance):
           smallestx,smallesty = x,y
           smallestdistance = distance
           smallesti = i
        i += 1
        
    smallestx,smallesty = circlepoints[(smallesti+1)%len(circlepoints)]
    #return boid.x-smallestx,boid.y-smallesty
    dirx,diry = 1,1
    
    if(smallestx<boid.x):
        dirx = -1
    if(smallesty<boid.y):
        diry = -1
    return dirx,diry

class Boid:
    def __init__(self):
        self.x = random.uniform(0,100)
        self.y = random.uniform(0,100)
        self.speedx = 1.0
        self.speedy = 1.0
        self.lastx = self.x-random.uniform(0.5,2)
        self.lasty = self.y-random.uniform(0.5,2)

    def move(self):
        self.lastx = self.x
        self.lasty = self.y
        self.x += self.speedx
        if(self.isCrashing()):
            self.x -= 2*self.speedx
        self.y += self.speedy
        if(self.isCrashing()):
            self.y -= 2*self.speedy
              

    def calcSpeed(self):
        hypotenuse = abs(math.sqrt((self.x-self.lastx)**2 + (self.y-self.lasty)**2))
        if(hypotenuse<0.5):
            hypotenus = 0.5
        if(hypotenuse>2):
            hypotenuse = 2
        catheti = math.sqrt((hypotenuse**2)/2)
        #catheti = 1 
        dirx,diry = getDirection(self) 
        self.speedx = dirx*catheti
        self.speedy = diry*catheti
#
#        if(self.x>80):
#            self.speedx = -catheti
#        if(self.x<20):
#            self.speedx = catheti
#        if(self.y>80):
#            self.speedy = -catheti
#        if(self.y<20):
#            self.speedy = catheti

    def avoidCrashOthers(self):
       i = 0
       while(self.isCrashing() and i<5):
            self.x += self.speedx
            self.y += self.speedy
            i += 1

    def isCrashing(self):
        for oneBoid in allboids:
             if oneBoid != self:
                  crash = True
                  if(self.x>oneBoid.x+2 or oneBoid.x>self.x+2):
                       crash = False
                  if(self.y>oneBoid.y+2 or oneBoid.y>self.y+2):
                       crash = False
                  if crash:
                       return True

    def getDistance(self,other):
        return abs(math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2))
       
    def getClosest(self):
        closestBoid = allboids[0]
        distance = self.getDistance(closestBoid)
        for oneBoid in allboids:
            if oneBoid != self:
                if(self.getDistance(oneBoid)<distance):
                      closestBoid = oneBoid
                      distance = self.getDistance(closestBoid)
        return closestBoid,distance
 
    def stayCloseToOthers(self):
        closestBoid,distance = self.getClosest()
        if(distance<50 and distance>20):
           if(closestBoid.x<self.x):
                self.x -= 1
           if(closestBoid.y<self.y):
                self.y -= 1
           if(closestBoid.x>self.x):
                self.x += 1
           if(closestBoid.y>self.y):
                self.y += 1
                      
    def mapClosestSpeed(self):
        closestBoid,distance = self.getClosest()
        if(distance<50):
            self.speedx = closestBoid.speedx
            self.speedy = closestBoid.speedy                   
        #print self.speedx   


allboids = [Boid() for i in range(100)]
def getNextBoids():
    for boid in allboids:
        boid.calcSpeed()
        boid.stayCloseToOthers()
        boid.move()
        #boid.avoidCrashOthers()
        boid.mapClosestSpeed()
    #return [b[0] for b in circlepoints],[b[1] for b in circlepoints]
    #print [(b.x,b.y) for b in allboids]
    return [(b.x,b.y) for b in allboids]#,[b.y for b in allboids]
