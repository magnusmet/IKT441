import random

class Node:
    def __init__(self,name):
        self.name = name
        self.edges = []
        
    def rouletteWheelSimple(self):
        return random.sample(self.edges,1)[0]
    
    def rouletteWheel(self,visitedEdges,startNode):
          visitedNodes = [oneEdge.toNode for oneEdge in visitedEdges]
          viableEdges = [oneEdge for oneEdge in self.edges if not oneEdge.toNode in visitedNodes and oneEdge.toNode!=startNode]
          if not viableEdges: 
               viableEdges = [oneEdge for oneEdge in self.edges if not oneEdge.toNode in visitedNodes]

          allPheromones = sum([oneEdge.pheromones for oneEdge in viableEdges])
          num = random.uniform(0,allPheromones)
          s = 0
          i = 0
          selectedEdge = viableEdges[i]
          while(s<=num):
              selectedEdge = viableEdges[i]
              s += selectedEdge.pheromones
              i += 1
          return selectedEdge
    
    def __repr__(self):
        return self.name
    
class Edge:
    def __init__(self,fromNode,toNode,cost):
        self.fromNode = fromNode
        self.toNode = toNode
        self.cost = cost
        self.pheromones = 1
        
    def __repr__(self):
       return self.fromNode.name + "--(" + str(self.cost) + ")--" + self.toNode.name

a = Node("A")
b = Node("B")
c = Node("C")
d = Node("D")
e = Node("E")
nodes = [a,b,c,d,e]

edges = [
   Edge(a,b,100),
   Edge(a,c,175),
   Edge(a,d,100),
   Edge(a,e,75),
   Edge(b,c,50),
   Edge(b,d,75),
   Edge(b,e,125),
   Edge(c,d,100),
   Edge(c,e,125),
   Edge(d,e,75)]

#Make symetrical
for oneEdge in edges[:]:
   edges.append(Edge(oneEdge.toNode,oneEdge.fromNode,oneEdge.cost))
  

#Assign to nodes
for oneEdge in edges:
    for oneNode in nodes:
        if(oneEdge.fromNode==oneNode):
            oneNode.edges.append(oneEdge)

def checkAllNodesPresent(edges):
    visitedNodes = [edge.toNode for edge in edges]
    return set(nodes).issubset(visitedNodes)

#Cost function
def getSum(edges):
    return sum(e.cost for e in edges)

MAXCOST = getSum(edges)

class ANT:
    def __init__(self):
        self.visitedEdges = []
        
    def walk(self,startNode):
        currentNode = startNode
        currentEdge = None
        while(not checkAllNodesPresent(self.visitedEdges)):
            #currentEdge = currentNode.rouletteWheelSimple()
            currentEdge = currentNode.rouletteWheel(self.visitedEdges,startNode)
            currentNode = currentEdge.toNode
            self.visitedEdges.append(currentEdge)
            
    def pheromones(self):
        currentCost = getSum(self.visitedEdges)
        score = 1000**(1-float(currentCost)/MAXCOST)
        for oneEdge in self.visitedEdges:
            oneEdge.pheromones += score

for i in range(10000):
    ant = ANT()
    ant.walk(a)
    ant.pheromones()
    print i,getSum(ant.visitedEdges)