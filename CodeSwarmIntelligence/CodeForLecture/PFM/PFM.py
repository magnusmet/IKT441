import math
import random

#det = True
det = raw_input("Deterministic?")=="y"

class Environment:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def distance(self,x,y):
        thisx = random.uniform(-1,1)+self.x
        thisy = random.uniform(-1,1)+self.y
        if det:
           thisx = self.x
           thisy = self.y
        return math.sqrt( (x - thisx)**2 + (y - thisy)**2 )

e = Environment(10,10)#random.uniform(0,100),random.uniform(0,100))
#print e.distance(11,11)
c1 = 0.5
c2 = 0.5
global gbest
global gbestx
global gbesty
gbest = 100*100
gbestx,gbesty = random.uniform(0,100),random.uniform(0,100)

class Particle:
    def __init__(self):
        self.x,self.y = random.uniform(0,100),random.uniform(0,100)
        self.pbestx,self.pbesty = self.x,self.y
        self.pbest = 100*100
        self.vx = 0
        self.vy = 0

    def updatePbest(self):
        d = e.distance(self.x,self.y)
        if(d<self.pbest):
             self.pbest = d
             self.pbestx,self.pbesty = self.x,self.y
        global gbestx
        global gbesty
        global gbest
        if(d<gbest):
             #print "Better"
             gbest = d
             gbestx,gbesty = self.x,self.y

    def calcVelocity(self):
        #Delta v
        r1 = random.uniform(-1,1)
        r2 = random.uniform(-1,1)
        deltav_x = r1*(self.pbestx-self.x) +  r2*(gbestx-self.x) 
        deltav_y = r1*(self.pbesty-self.y) +  r2*(gbesty-self.y) 
        #V
        self.vx = deltav_x
        self.vy = deltav_y

    def move(self):
        #S
        self.x += self.vx
        self.y += self.vy

particles = [Particle() for i in range(1000)]


def getGlobalDistance():
    return sum([e.distance(p.x,p.y) for p in particles])

def getNextParticles():
    for p in particles:
        p.updatePbest()
    for p in particles:
        p.calcVelocity()
        p.move()
    print i,getGlobalDistance(),gbest,gbestx,gbesty
    return [(p.x,p.y) for p in particles]#,[p.y for p in particles]

#print getGlobalDistance()
           

if __name__=="__main__":
   e = Environment(10,10)
   print e.distance(100,100)
