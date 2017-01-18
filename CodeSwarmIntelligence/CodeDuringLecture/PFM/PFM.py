import math
import random

class Environment:
    def __init__(self,x,y):
         self.x = x
         self.y = y
 
    def distance(self,x,y):
         return math.sqrt((x-self.x)**2 + (y-self.y)**2)

e = Environment(10,10)

global gbest,gbestx,gbesty
gbest = 100*100
gbestx,gbesty = random.uniform(0,100),random.uniform(0,100)
C1 = 0.5
C2 = 0.5

class Particle:
    def __init__(self):
        self.x,self.y = random.uniform(0,100),random.uniform(0,100)
        self.pbestx,self.pbesty = self.x,self.y
        self.pbest = 100*100

    def updateBest(self):
        d = e.distance(self.x,self.y)
        if(d<self.pbest):
             self.pbest = d
             self.pbestx = self.x
             self.pbesty = self.y
        global gbest,gbestx,gbesty
        if(d<gbest):
             gbest = d
             gbestx = self.x
             gbesty = self.y

    def calcVelocity(self):
        w1 = C1*random.uniform(-1,1)
        w2 = C2*random.uniform(-1,1)
        self.v_x = w1*(self.pbestx-self.x) + w2*(gbestx-self.x)
        self.v_y = w1*(self.pbesty-self.y) + w2*(gbesty-self.y)

    def move(self):
        self.x += self.v_x
        self.y += self.v_y
        

particles = [Particle() for i in range(1000)]

def getNextParticles():
   for p in particles:
       p.updateBest()
   for p in particles:
       p.calcVelocity()
       p.move()


   return [(p.x,p.y) for p in particles]
