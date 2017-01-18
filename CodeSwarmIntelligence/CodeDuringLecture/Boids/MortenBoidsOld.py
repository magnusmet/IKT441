import math
import random

class Boid:
   def __init__(self):
       self.x = random.uniform(0,100)
       self.y = random.uniform(0,100)
       self.speedx = 1.0
       self.speedy = 1.0
       self.lastx = self.x-1
       self.lasty = self.y-1

   def move(self):
       self.lastx = self.x
       self.lasty = self.y
       self.x += self.speedx
       self.y += self.speedy

   def calcSpeed(self):
       hypothenuse = abs(math.sqrt((self.x-self.lastx)**2 + (self.y-self.lasty)**2))
       if(hypothenuse<0.5):
           hypothenuse = 0.5
       if(hypothenuse>2):
           hypothenuse = 2
       catheti = math.sqrt((hypothenuse**2)/2)
       if(self.x>80):
           self.speedx = - catheti
       if(self.x<20):
           self.speedx = catheti
       if(self.y>80):
           self.speedy = - catheti
       if(self.y<20):
           self.speedy = catheti

   def avoidCrash(self):
       while(self.isCrashing()):
           self.x += self.speedx
           self.y += self.speedy

   def isCrashing(self):
      for oneBoid in allboids:
          if(oneBoid != self):
              crash = True
              if(self.x>oneBoid.x+2 or oneBoid.x > self.x +2):
                  crash = False
              if(self.y>oneBoid.y+2 or oneBoid.y > self.y +2):
                  crash = False
              if(crash):
                  return True
      return False

   def getDistance(self,other):
      return abs(math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2))

   def getClosest(self):
      closestBoid = allboids[0]
      distance = self.getDistance(closestBoid)
      for oneBoid in allboids:
          if(oneBoid != self):
              if(self.getDistance(oneBoid)<distance):
                  closestBoid = oneBoid
                  distance = self.getDistance(oneBoid)
      return closestBoid,distance

   def stayCloseToOthers(self):
       closestBoid,distance = self.getClosest()
       if(distance<5 and distance>2):
           if(closestBoid.x<self.x):
               self.x -= 1
           if(closestBoid.x>self.x):
               self.x += 1
           if(closestBoid.y<self.y):
               self.y -= 1
           if(closestBoid.y>self.y):
               self.y += 1

   def mapClosestSpeed(self):
       closestBoid,distance = self.getClosest()
       if(distance<5):
           self.speedx = closestBoid.speedx
           self.speedy = closestBoid.speedy
 

allboids = [Boid() for i in range(100)]

def getNextBoids():
    for boid in allboids:
        boid.mapClosestSpeed()
        boid.calcSpeed()
        boid.move()
        boid.avoidCrash()
        boid.stayCloseToOthers()
    return [(b.x,b.y) for b in allboids]
