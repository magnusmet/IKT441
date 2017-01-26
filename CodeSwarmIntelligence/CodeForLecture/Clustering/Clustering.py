import random
import math

class Node:
    def __init__(self,x,y,cluster):
        self.x = x#20+x#x
        self.y = y#40+y#$y
        self.cluster = cluster
       

NCLUSTERS = 3

data = [Node(random.uniform(0,100),random.uniform(0,100),random.randint(0,NCLUSTERS-1)) for i in range(1000)]

def getDistance(xone,yone,xtwo,ytwo):
     return abs(math.sqrt((xone-xtwo)**2 + (yone-ytwo)**2))

def kmeans():
    global data
    centroids = {}
    for cluster in range(NCLUSTERS):
        thisdata = [n for n in data if n.cluster==cluster]
        avgx = sum([n.x for n in thisdata])/len(thisdata) 
        avgy = sum([n.y for n in thisdata])/len(thisdata)
        print cluster,len(thisdata) 
        centroids[cluster] = (avgx,avgy)
    print centroids
   
    for node in data:
        distance = 100000
        for c,coordinate in centroids.items():
            if(getDistance(node.x,node.y,coordinate[0],coordinate[1])<distance):
                 closestcluster = c
                 distance = getDistance(node.x,node.y,coordinate[0],coordinate[1])
        node.cluster = closestcluster
    return centroids


def getNextData():
     centroids = kmeans()
     return [(n.x,n.y) for n in data if n.cluster==0],[(n.x,n.y) for n in data if n.cluster==1],[(n.x,n.y) for n in data if n.cluster==2]
     #return [(i[0],i[1]) for i in centroids.values()],[(n.x,n.y) for n in data if n.cluster==0],[(n.x,n.y) for n in data if n.cluster==1],[(n.x,n.y) for n in data if n.cluster==2]
