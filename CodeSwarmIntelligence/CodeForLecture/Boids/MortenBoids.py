import random
import math

class Boid:
    def __init__(self):
        self.y = random.uniform(0,100)
        self.x = random.uniform(0,100)
        self.movementx = 1.0
        self.movementy = 1.0
        self.lastx = self.x-1
        self.lasty = self.y-1
    
    def getDistance(self,other):
        return abs(math.sqrt( (self.x - other.x)**2 + (self.y - other.y)**2 ))
    
        
    def calcSpeed(self):
        self.speed = abs(math.sqrt( (self.x - self.lastx)**2 + (self.y - self.lasty)**2 ))
        if self.speed< 0.5:
            self.speed = 0.5
        if self.speed> 2:
            self.speed = 2

        #print "Speed:",self.speed
        if(self.x>80):
            self.movementx = -math.sqrt((self.speed**2)/2)
        if(self.x<20):
            self.movementx = math.sqrt((self.speed**2)/2)
        if(self.y>80):
            self.movementy = -math.sqrt((self.speed**2)/2)
        if(self.y<20):
            self.movementy = math.sqrt((self.speed**2)/2)
        #self.lastx = self.x
        #self.lasty = self.y
        
 
    def move(self):
        self.lastx = self.x
        self.lasty = self.y
        self.x += self.movementx
        self.y += self.movementy
        if(self.crashOthers()):
            self.x -= self.movementx
            self.y -= self.movementy
        #self.calcSpeed()


    def avoidCrashOthers(self):
        i = 0
        while(self.crashOthers() and i<5):
             i+=1
             #self.movementy = - self.movementy
             #self.movementx = - self.movementx
             #print "Crashing"
             self.x+=self.movementx#random.sample([-self.movementx,self.movementx],1)[0]
             self.y+=self.movementy#random.sample([-self.movementy,self.movementy],1)[0]
             #self.movementx *=2
             #self.movementy *=2
    def avoidOutsideBoard(self):
        if(self.x<0):
             #self.x = 100
             self.movementx = abs(self.movementx)
             self.x+=1
        if(self.x>100):
             #self.x = 0
             self.movementx = -abs(self.movementx)
             self.x-=1
        if(self.y<0):
             #self.y = 100
             self.movementy = abs(self.movementy)
             self.y +=1
        if(self.y>100):
             #self.y = 0
             self.movementy = -abs(self.movementy)
             ##self.y -=1

    def mapSpeedToClosest(self):
        closestBoid = allboids[0]
        distance = self.getDistance(closestBoid)
        for oneBoid in allboids:
           if oneBoid != self:
               if(self.getDistance(oneBoid)<distance):
                   closestBoid = oneBoid
                   distance = self.getDistance(oneBoid)
        if(distance<10):
           self.movementx = closestBoid.movementx
           self.movementy = closestBoid.movementy
             

    def stayCloseToOthers(self):
        closestBoid = allboids[0]
        distance = self.getDistance(closestBoid)
        for oneBoid in allboids:
           if oneBoid != self:
               if(self.getDistance(oneBoid)<distance):
                   closestBoid = oneBoid
                   distance = self.getDistance(oneBoid)
        if(distance<5):
           if(closestBoid.x<self.x):
                self.x -= 1
           if(closestBoid.x>self.x):
                self.x += 1
           if(closestBoid.y<self.y):
                self.y -= 1
           if(closestBoid.y>self.y):
                self.y += 1
 
    def crashOthers(self):
        for oneBoid in allboids:
           if oneBoid != self:
               crash = True
               if(self.x>oneBoid.x+2 or oneBoid.x>self.x+2):
                   crash = False
               if(self.y>oneBoid.y+2 or oneBoid.y>self.y+2):
                   crash = False
               if crash:
                    return True


allboids = [Boid() for i in range(100)]


def getNextBoids():
    #random.shuffle(allboids)
    for boid in allboids:
        boid.mapSpeedToClosest()
        boid.calcSpeed()
        boid.move()
        boid.avoidCrashOthers()
        boid.stayCloseToOthers()
        #boid.avoidOutsideBoard()
    return [(b.x,b.y) for b in allboids]#,[b.y for b in allboids]
