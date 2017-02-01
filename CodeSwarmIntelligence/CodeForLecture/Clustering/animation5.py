import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

import Clustering
t=0
r=3.0
n=0
global centroids,one,two,three

def startNew():
    global centroids,one,two,three
    centroids=[]
    one=[]
    two=[]
    three=[]
    for x in range(10):
        for y in range(10):

            #centroids.append([random.uniform(0,100),random.uniform(0,100)])
            one.append([random.uniform(0,100),random.uniform(0,100)])
            two.append([random.uniform(0,100),random.uniform(0,100)])
            three.append([random.uniform(0,100),random.uniform(0,100)])
    #centroids = np.array(centroids).transpose()
    one = np.array(one).transpose()
    two = np.array(two).transpose()
    three = np.array(three).transpose()



def start(en,to,tre):
    global centroids,one,two,three
    #import pdb;pdb.set_trace()
    #centroids=[[i[0],i[1]] for i in centroids]
    one=[[i[0],i[1]] for i in en]
    two=[[i[0],i[1]] for i in to]
    three=[[i[0],i[1]] for i in tre]
    #centroids = np.array(centroids)#.transpose()
    one = np.array(one)#.transpose()
    two = np.array(two)#.transpose()
    three = np.array(three)#.transpose()
    print "Start",len(one)#,
    
    return one,two,three
startNew()
fig = plt.figure()
#linecentroids, = plt.plot(centroids[0],centroids[1], "ro", color="blue")
lineone, = plt.plot(one[0],one[1], "ro", color="green")
linetwo, = plt.plot(two[0],two[1], "ro", color="red")
linethree, = plt.plot(three[0],three[1], "ro", color="yellow")

def update():
    while(True):
        #import pdb;pdb.set_trace()
        d = Clustering.getNextData()
        #A[0],A[1] = np.array([d[0],d[1]])
        en,to,tre = start(d[0],d[1],d[2])
        #centroids[0],centroids[1] = np.array([c[0],c[1]])
        one[0],one[1] = np.array([en[0],en[1]])
        two[0],two[1] = np.array([to[0],to[1]])
        three[0],three[1] = np.array([tre[0],tre[1]])
        #centroids[0],centroids[1] = np.array([d[0],d[1]])
        #one[0],one[1] = np.array([d[2],d[3]])
        #two[0],two[1] = np.array([d[4],d[5]])
        #three[0],three[1] = np.array([d[6],d[7]])

        yield one,two,three
    #d = Clustering.getNextData()
    #for i in range(len(d[0])):
    #    A[0],A[1] = d[0][i],d[1][i]
    #for i in range(100):
    #    A[0], A[1] = r*A[0]*(1-A[0]), r*A[1]*(1-A[1])
    #    print A
    #    yield A

def draw(data):
    #print "Draw data",data
    #linecentroids.set_xdata(data[0][0])
    #linecentroids.set_ydata(data[0][1])
    print "Draw",len(data[1])
    #linecentroids.set_xdata([i[0] for i in data[0]])
    #linecentroids.set_ydata([i[1] for i in data[0]])
    lineone.set_xdata([i[0] for i in data[0]])
    lineone.set_ydata([i[1] for i in data[0]])
    linetwo.set_xdata([i[0] for i in data[1]])
    linetwo.set_ydata([i[1] for i in data[1]])
    linethree.set_xdata([i[0] for i in data[2]])
    linethree.set_ydata([i[1] for i in data[2]])
    return lineone,linetwo,linethree

ani = animation.FuncAnimation(fig, draw, update, interval=1000, blit=False)

plt.show()
