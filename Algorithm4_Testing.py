##
## Testing Code for the Gossip Algorithm Implementations
##
## CMSC 641, Fall 2013 semester project
##
## Authors: Karan Budhraja, John Winder, Siddharth Pramod
##
################################# imports ######################################
# display original source code:
# https://www.udacity.com/wiki/creating%20network%20graphs%20with%20python

import random
from time import time
from collections import deque
from math import fabs
import networkx

################################# globals ######################################

# K is the size of neighborhood around each vertex
# so when algorithm completes each vertex knows rumors from all verticess 
# k hops away
K = 1                               # for the 1 local broadcast problem, K is 1

RUNS_FOR_AVERAGE = 25               # number of runs to be averaged over

# these are tunable parameters
MAX_NUMBEROFNODES = 1000            # maximum number of nodes in graph
MAX_I = 10                          # maximum value of i for an i-tree

THRESHOLD = 0.8
P_CONNECITON = 0.5                  # random.uniform(0,1) for pure randomness
P_RUMOR = 1                         # assuming that each node has a rumor
RUMOR_LOWER_BOUND = 0               # bounds of value associated with rumor
RUMOR_UPPER_BOUND = 100

gRounds = 0                         # track number of rounds and iterations
gIterations = 0

NODE_NUMBER = 1                     # starting value for manual node numbering

################################ classes #######################################

class Rumor(object):                # rumor as an object

    global RUMOR_LOWER_BOUND
    global RUMOR_UPPER_BOUND

    LOWERBOUND = RUMOR_LOWER_BOUND  # bounds for random number generation
    UPPERBOUND = RUMOR_UPPER_BOUND

    def __init__(self, origin, value):
        self.origin = origin        # node to which rumor belongs
        self.value = value          # value associated with rumor

    def __str__(self):
        return "(" + str(self.origin) + ", " + self.value + ")"

    def __repr__(self):
        return self.__str__()

    def __eq__(self,other):
        return self.origin == other.origin

    def __hash__(self):
        return hash(self.origin)

class Vertex(object):               # node as an object

    def __init__(self, identity, rumors, neighbors):
        self.identity = identity
        self.rumors = rumors
        self.neighbors = neighbors
        self.orderedLinks = []
        self.rPrime = set()         # as per Haeupler's Algorithm
        self.rDoublePrime = set()
        self.received = set()

    def summary(self):
        return str(self.identity) + " " + str(self.rumors) + " " + str(self.rPrime) \
            + " " + str(self.rDoublePrime) + " " + str(self.received) \
            + " " + str([n for n in self.neighbors])

    # added while shifting from gephi
    def make_neighbors(self, neighbor):
        self.neighbors.add(neighbor.identity)
        neighbor.neighbors.add(self.identity)

    # test if rumorSet is in vertex's set of rumors
    def has_rumors(self, rumorSet):
        result = len(rumorSet.difference(self.rumors)) == 0
        return result

    def get_unlinked_neighbor(self):

        rumorIds = set([r.origin for r in self.rumors])
        linkedIds = set([v for v in self.orderedLinks])

        selectionSet = self.neighbors.difference(linkedIds.union(rumorIds))

        # return false if no valid unlinked neighbor
        if (len(selectionSet) < 1):
            return False

        # choosing randomly
        uID = random.sample(selectionSet, 1)[0]

        return uID

    def get_unlinked_neighbor_higher_first(self):

        rumorIds = set([r.origin for r in self.rumors])
        linkedIds = set([v for v in self.orderedLinks])

        selectionSet = self.neighbors.difference(linkedIds.union(rumorIds))

        # return false if no valid unlinked neighbor
        if (len(selectionSet) < 1):
            return False

 #       print(self.identity, selectionSet)

        # choosing randomly
        uID = random.sample(selectionSet, 1)[0]

        # using a heuristic now 
        selectionList = list(selectionSet)
        selectionList.sort()

        uIDFound = False

        if uIDFound  == False:            
            # get the first element which is greater than, if any
        
            for item in selectionList:
                if uIDFound == False:
                    if item > self.identity:
                        uID = item
                        uIDFound = True
                    
        if uIDFound  == False:            
            # else, get the first element which is less than

            # reverse selection list
            selectionList = selectionList[::-1]
            
            for item in selectionList:
                if uIDFound == False:
                    if item < self.identity:
                        uID = item
                        uIDFound = True

        return uID
    
    def get_unlinked_neighbor_lower_first(self):

        rumorIds = set([r.origin for r in self.rumors])
        linkedIds = set([v for v in self.orderedLinks])

        selectionSet = self.neighbors.difference(linkedIds.union(rumorIds))

        # return false if no valid unlinked neighbor
        if (len(selectionSet) < 1):
            return False

        # choosing randomly
        uID = random.sample(selectionSet, 1)[0]

        # using a heuristic now 
        selectionList = list(selectionSet)
        selectionList.sort()

        uIDFound = False
                    
        if uIDFound  == False:            
            # else, get the first element which is less than

            # reverse selection list
            selectionList = selectionList[::-1]
            
            for item in selectionList:
                if uIDFound == False:
                    if item < self.identity:
                        uID = item
                        uIDFound = True

        if uIDFound  == False:            
            # get the first element which is greater than, if any
  
            # reverse selection list
            selectionList = selectionList[::-1]
        
            for item in selectionList:
                if uIDFound == False:
                    if item > self.identity:
                        uID = item
                        uIDFound = True

        return uID

    def get_unlinked_closest(self):

        rumorIds = set([r.origin for r in self.rumors])
        linkedIds = set([v for v in self.orderedLinks])

        selectionSet = self.neighbors.difference(linkedIds.union(rumorIds))

        # return false if no valid unlinked neighbor
        if (len(selectionSet) < 1):
            return False
           
        selectionSet = sorted(selectionSet, key=lambda x: fabs(x-self.identity))
        uID = selectionSet[0]

        return uID

    def get_unlinked_cyclic(self):

        rumorIds = set([r.origin for r in self.rumors])
        linkedIds = set([v for v in self.orderedLinks])

        selectionSet = self.neighbors.difference(linkedIds.union(rumorIds))

        # return false if no valid unlinked neighbor
        if (len(selectionSet) < 1):
            return False

        # choosing randomly
        uID = random.sample(selectionSet, 1)[0]

        # using a heuristic now 
        selectionList = list(selectionSet)
        selectionList.sort()

        uIDFound = False

        if uIDFound  == False:            
            # get the first element which is greater than, if any
        
            for item in selectionList:
                if uIDFound == False:
                    if item > self.identity:
                        uID = item
                        uIDFound = True
                    
        if uIDFound  == False:            
            # else, get the first element which is less than
            
            for item in selectionList:
                if uIDFound == False:
                    if item < self.identity:
                        uID = item
                        uIDFound = True

        return uID

    def get_unlinked_lowest(self):

        rumorIds = set([r.origin for r in self.rumors])
        linkedIds = set([v for v in self.orderedLinks])

        selectionSet = self.neighbors.difference(linkedIds.union(rumorIds))

        # return false if no valid unlinked neighbor
        if (len(selectionSet) < 1):
            return False

        # using a heuristic now 
        selectionList = list(selectionSet)
        selectionList.sort()

        # the first element will be the same for all except 1 vertex
        uID = selectionList[0]

        return uID
        
    def link_to(self,node):
        self.orderedLinks.append(node)

    # push and pull use this
    def exchange_rumors(self,rumorSet,neighbor):

        # combine rPrime or rDoublePrime with neighbor's rumors

        u = rumorSet.union(neighbor.rumors)

        # add it to the neighbor's set of received rumors for this round
        neighbor.received = u.union(neighbor.received)

        # return union which is set to rPrime or rDoublePrime
        return u

    def refresh(self):
        # add the rumors received during round
        self.rumors = self.rumors.union(self.received)
        # clear received set
        self.received = set()


class Graph(object):

    def __init__(self, vertices):
        self.vertices = vertices

    def get_node(self, identity):
        out = False
        for vertex in self.vertices:
            if (identity == vertex.identity):
                out = vertex
                break
        return out

    def get_diameter(self):

        # map to networkx graph
        
        graph = networkx.Graph()
        
        for vertex in self.vertices:
            graph.add_node(vertex.identity)
        
        # networkx takes care of not repeating edges for to and fro
        for vertex in self.vertices:
            for neighbor in vertex.neighbors:
                graph.add_edge(vertex.identity, neighbor)
        
        # get diameter of networkx graph
        diameter = networkx.diameter(graph)

        return diameter

    def display(self):

        vList = [v for v in self.vertices]
        vList.sort(key=lambda x: x.identity)

        print("")
        print("--------------------------")
        for vertex in vList:
            print(vertex.summary())

################################ functions #####################################

def is_finished(verts):             # check to see if algorithm is completed

    # return true only if all vertices have k rumors
    for vertex in verts:
        for n in vertex.neighbors:
            rumorIds = [r.origin for r in vertex.rumors]
            if n not in rumorIds:
                return False
    return True
    
def generate_i_tree(i):
    
    global NODE_NUMBER

    root = None
    
    # generate i-tree

    allRumors = set()
    vertices = []    
    
    if i == 1:
        # base case
        
        # create a vertex
        nodeNumber = NODE_NUMBER + 1
        NODE_NUMBER += 1
        
        # no edges right now
        edgeListG = set()

        # populate rumors if any
        nodeRumorSet = set()
                                    # random number between 0 and 1
        pNodeRumor = random.uniform(0,1)
        if pNodeRumor < P_RUMOR:
            value = str(random.randint(RUMOR_LOWER_BOUND, RUMOR_UPPER_BOUND))
                                    # nodes have rumors at random
            nodeRumor = Rumor(nodeNumber, value)                                        
            nodeRumorSet.add(nodeRumor)
            allRumors.add(nodeRumor)

        else:
            nodeRumor = set()

        # create a vertex
        vertex = Vertex(nodeNumber, nodeRumorSet, edgeListG)
        vertices.append(vertex)

        root = vertex
        
    else:
        [root1, graph1, allRumors1] = generate_i_tree(i-1)
        [root2, graph2, allRumors2] = generate_i_tree(i-1)

        root = root1
        root1.make_neighbors(root2)
    
        # combine graph vertices into a single list
        for vertex in graph1.vertices:
            vertices.append(vertex)
        
        for vertex in graph2.vertices:
            vertices.append(vertex)
        
        # combine rumors
        allRumors = allRumors1.union(allRumors2)
    
    # create graph
    graph = Graph(vertices)

    return [root, graph, allRumors]

def generate_random_graph(numberOfNodes):

    global P_CONNECITON

    global P_RUMOR
    global RUMOR_LOWER_BOUND
    global RUMOR_UPPER_BOUND

    # generate random graph

    allRumors = set()
    vertices = []

    # create nodes
    for i in range(numberOfNodes):

        # no edges right now
        edgeListG = set()

        # populate rumors if any
        nodeRumorSet = set()

        pNodeRumor = random.uniform(0,1)                                        
                                    # random number between 0 and 1
        if pNodeRumor < P_RUMOR:
            value = str(random.randint(RUMOR_LOWER_BOUND, RUMOR_UPPER_BOUND))
            nodeRumor = Rumor(i+1, value)                                        
                                    # nodes have rumors at random
            nodeRumorSet.add(nodeRumor)
            allRumors.add(nodeRumor)
        else:
            nodeRumor = set()

        # create a vertex
        vertex = Vertex(i+1, nodeRumorSet, edgeListG)
        vertices.append(vertex)

    # populate edges
    connected = []
    connected.append(vertices[0])

    for u in vertices:

        if(u in connected):
            continue
        v = random.choice(connected)

        u.make_neighbors(v)
        connected.append(u)
        if(len(connected) > numberOfNodes * THRESHOLD):
            for w in vertices:
                if(random.random() < P_CONNECITON and not w in connected):
                    u.make_neighbors(w)

    # create graph
    graph = Graph(vertices)

    return [graph, allRumors]

def generate_star_graph(numberOfNodes):

    global P_RUMOR
    global colorList
    global RUMOR_LOWER_BOUND
    global RUMOR_UPPER_BOUND

    # generate star graph

    allRumors = set()
    vertices = []

    # create nodes
    for i in range(numberOfNodes):

        # no edges right now
        edgeListG = set()

        # populate rumors if any
        nodeRumorSet = set()

        pNodeRumor = random.uniform(0,1)                                        
                                    # random number between 0 and 1
        if pNodeRumor < P_RUMOR:
            value = str(random.randint(RUMOR_LOWER_BOUND, RUMOR_UPPER_BOUND))
            nodeRumor = Rumor(i+1, value)                        
                                    # nodes have rumors at random
            nodeRumorSet.add(nodeRumor)
            allRumors.add(nodeRumor)
        else:
            nodeRumor = set()

        # create a vertex
        vertex = Vertex(i+1, nodeRumorSet, edgeListG)
        vertices.append(vertex)

    # populate edges

    # just take one node and use make_neighbors with all other nodes
    u = vertices[0]
    
    for v in vertices:
        if u != v:
            u.make_neighbors(v)
        
    # create graph
    graph = Graph(vertices)

    return [graph, allRumors]
    
def generate_complete_graph(numberOfNodes):

    global P_RUMOR
    global RUMOR_LOWER_BOUND
    global RUMOR_UPPER_BOUND

    # generate complete graph

    allRumors = set()
    vertices = []

    # create nodes
    for i in range(numberOfNodes):

        # no edges right now
        edgeListG = set()

        # populate rumors if any
        nodeRumorSet = set()

        pNodeRumor = random.uniform(0,1)                                        
                                    # random number between 0 and 1
        if pNodeRumor < P_RUMOR:
            value = str(random.randint(RUMOR_LOWER_BOUND, RUMOR_UPPER_BOUND))
            nodeRumor = Rumor(i+1, value)                                        
                                    # nodes have rumors at random
            nodeRumorSet.add(nodeRumor)
            allRumors.add(nodeRumor)
        else:
            nodeRumor = set()

        # create a vertex
        vertex = Vertex(i+1, nodeRumorSet, edgeListG)
        vertices.append(vertex)

    # populate edges

    # just take one node and use make_neighbors with all other nodes
    u = vertices[0]
    
    for u in vertices:
        for v in vertices:
            if u != v:
                u.make_neighbors(v)
            
    # create graph
    graph = Graph(vertices)

    return [graph, allRumors]

    
def generate_linear_graph(numberOfNodes):

    global P_CONNECITON

    # generate linear graph

    allRumors = set()
    vertices = []

    # create nodes
    for i in range(numberOfNodes):

        # no edges right now
        edgeListG = set()

        # populate rumors if any
        nodeRumorSet = set()

        pNodeRumor = random.uniform(0,1)                                        
                                    # random number between 0 and 1
        if pNodeRumor < P_RUMOR:
            value = str(random.randint(RUMOR_LOWER_BOUND, RUMOR_UPPER_BOUND))
            nodeRumor = Rumor(i+1, value)                                        
                                    # nodes have rumors at random
            nodeRumorSet.add(nodeRumor)
            allRumors.add(nodeRumor)
        else:
            nodeRumor = set()

        # create a vertex
        vertex = Vertex(i+1, nodeRumorSet, edgeListG)
        vertices.append(vertex)

    # populate edges
    u = vertices[0]

    for v in vertices:
        if u == v:
            continue
        u.make_neighbors(v)
        u = v

    # create graph
    graph = Graph(vertices)

    return [graph, allRumors]

def push_pull(graph,i,push,rPrime):
    global gRounds

    numIterations = range(i+1)

    if(push):
        numIterations = [x for x in reversed(numIterations)]

    hadRound = False
    for j in numIterations:
        for vertex in graph.vertices:
            if(j < len(vertex.orderedLinks)):
            
                if(hadRound == False):
                    hadRound = True
                    gRounds += 1

                u_j = graph.get_node(vertex.orderedLinks[j])

                if(rPrime):
                    vertex.rPrime = vertex.exchange_rumors(vertex.rPrime,u_j)
                else:
                    vertex.rDoublePrime = vertex.exchange_rumors(vertex.rDoublePrime,u_j)

    for vertex in graph.vertices:
        vertex.refresh()

def spread_rumors(graph):
    global gIterations, gRounds

    i = 0

    # til the rumors have not been spread through the entire graph
    while(not is_finished(graph.vertices)):

        # each vertex link to new neighbor if able
        for vertex in graph.vertices:
            u_t = vertex.get_unlinked_neighbor()
#            u_t = vertex.get_unlinked_neighbor_higher_first()
#            u_t = vertex.get_unlinked_neighbor_lower_first()
#            u_t = vertex.get_unlinked_closest()
#            u_t = vertex.get_unlinked_cyclic()
#            u_t = vertex.get_unlinked_lowest()

            if (not (u_t == False)):
                vertex.link_to(u_t)

        push = True
        pull = False
        rPrime = True
        rDoublePrime =  False

        for vertex in graph.vertices:
            # R' = v
            vertex.rPrime = set()
            vertex.rPrime.update(vertex.rumors)
            # clear received rumors
            vertex.received = set()

        push_pull(graph,i,push,rPrime)
        push_pull(graph,i,pull,rPrime)

        for vertex in graph.vertices:
            # R'' = v
            vertex.rDoublePrime = set()
            vertex.rDoublePrime.update(vertex.rumors)
            # clear received rumors
            vertex.received = set()

        push_pull(graph,i,pull,rDoublePrime)
        push_pull(graph,i,push,rDoublePrime)

        for vertex in graph.vertices:
            vertex.rumors = vertex.rPrime.union(vertex.rDoublePrime)
            vertex.rPrime = set()
            vertex.rDoublePrime = set()
            vertex.received = set()

        i += 1
        gIterations = i

    return graph

################################## main ########################################

def run_algorithm(numberOfNodes):
    global gIterations, gRounds, K

    gIterations = 0
    gRounds = 0
    
    [graph, allRumors] = generate_random_graph(numberOfNodes)
#    [graph, allRumors] = generate_complete_graph(numberOfNodes)
#    [graph, allRumors] = generate_star_graph(numberOfNodes)
#    [graph, allRumors] = generate_linear_graph(numberOfNodes)
#    [root, graph, allRumors] = generate_i_tree(numberOfNodes)    # assume that numberOfNodes means i here

    # spread all rumors
    graph = spread_rumors(graph)

    return graph

def run_main(fTime):
    global gIterations, gRounds

    durations = deque([])

    iList = []
    diameterList = []
    roundsList = []
    iterationsList = []

    for i in range(10,MAX_NUMBEROFNODES+1,10):
#    for i in range(1,MAX_I+1):     # for i-trees    
        print(i)
        graph = run_algorithm(i)

        diameter = graph.get_diameter()
                
        iterations = gIterations
        rounds = gRounds
        
        iList.append(i)
        diameterList.append(diameter)
        roundsList.append(rounds)
        iterationsList.append(iterations)
        
#    return [iList, iterationsList, roundsList]
    return [iList, diameterList, iterationsList, roundsList]

########################### end of definitions #################################

def main():
    global RUNS_FOR_AVERAGE

    fTime = open('./Alorithm4_Haeupler_Time.txt', 'w')
    fTime.write("nodes,iterations,rounds\n")

    runList = []

    for i in range(RUNS_FOR_AVERAGE):
        [iList, diameterList, iterationsList, roundsList] = run_main(fTime)

        currentRun = [iList, diameterList, iterationsList, roundsList]
        runList.append(currentRun)

    averageRun = []

    for itemIndex in range(len(currentRun)):
        averageRun.append([])

    # number of items in currenRun
    for itemIndex in range(len(currentRun)):
        for i in range(len(iList)):
        
            total = 0
            
            for run in range(len(runList)):
                total += runList[run][itemIndex][i]
            
            average = total/len(runList)

            averageRun[itemIndex].append(average)


    for i in range(len(iList)):
        fTime.write(str(averageRun[0][i]) + "," + str(averageRun[1][i]) \
        + "," + str(averageRun[2][i]) + "," + str(averageRun[3][i]) + "\n")
#        fTime.write(str(2**averageRun[0][i]) + "," + str(averageRun[1][i]) \
#        + "," + str(averageRun[2][i]) + "\n")

    fTime.close()

main()
