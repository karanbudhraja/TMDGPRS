##
## Code for the Gossip Algorithm Implementations
##
## CMSC 641, Fall 2013 semester project
##
## Authors: Karan Budhraja, John Winder, Siddharth Pramod
##
################################# imports ######################################
# display original source code:
# https://www.udacity.com/wiki/creating%20network%20graphs%20with%20python

import random
from copy import deepcopy

################################# globals ######################################

colorList = {}                      # node coloring

# K is the size of neighborhood around each vertex
# so when algorithm completes each vertex knows rumors from all verticess 
# k hops away
K = 1                               # for the 1 local broadcast problem, K is 1

# these are tunable parameters
NUMBEROFNODES = 50 					# maximum number of nodes in graph
THRESHOLD = 0.8
pConnection = 0.5                   # random.uniform(0,1) for pure randomness
pRumor = 1                          # every node has its own rumor
RUMOR_LOWER_BOUND = 0
RUMOR_LOWER_BOUND = 100

R_VALUE_INDEX = 0                   # color indices
G_VALUE_INDEX = 1
B_VALUE_INDEX = 2
COLOR_VALUE_BOUND = 255

G_LAYOUT = ForceAtlas               # Gephi specific parameters
G_LAYOUT_ITERATIONS = 500
gNodeSize = 2.0

gRounds = 0                         # round and iteration of algorithm
gIterations = 0
    
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
        return str(self.identity) + " " + str(self.rumors) \
        + " " + str(self.rPrime) + " " + str(self.rDoublePrime) \
        + " " + str(self.received) 

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

    def display(self):
    
        vList = [v for v in self.vertices]
        vList.sort(key=lambda x: x.identity)
    
        print("")
        print("--------------------------")
        for vertex in vList:
            vertex.display()

    def draw(self):
       
        global R_VALUE_INDEX
        global G_VALUE_INDEX
        global B_VALUE_INDEX
        
        for node in g.nodes:    
            # get node with that ID
            # using very inefficient method right now. 
            # fix this later using filters
            for vertex in self.vertices:
                if(node.node == vertex.identity):
                    # got the corresponding node in g                        
                    # set rumors attribute
                    rumorString = "#"

                    rValueTotal = 0
                    gValueTotal = 0
                    bValueTotal = 0
                    
                    for rumor in vertex.rumors:
                        # concatenate all rumors
                        rumorString += str(rumor) + "#"
                    
                        # add rumor colors to get combine color
                        rValueTotal += colorList[rumor.origin][R_VALUE_INDEX]
                        gValueTotal += colorList[rumor.origin][G_VALUE_INDEX]
                        bValueTotal += colorList[rumor.origin][B_VALUE_INDEX]
                    
                    # done separately for clarity
                    if len(vertex.rumors) > 0:
                        # node has rumors
                        rValue = rValueTotal // len(vertex.rumors)
                        gValue = gValueTotal // len(vertex.rumors)
                        bValue = bValueTotal // len(vertex.rumors)
                        
                        # color nodes as per rumors
                        node.color = color(rValue, gValue, bValue)
                    else:
                        node.color = white
                        
                    node.Rumors = rumorString                
             
################################ functions #####################################
             
def is_finished(verts):

    # return true only if all vertices have k rumors
    for vertex in verts:

        for n in vertex.neighbors:
            rumorIds = [r.origin for r in vertex.rumors]
            if n not in rumorIds:
                return False
    return True

def get_color(nodeID):
    
    # generate color based on node ID
    global COLOR_VALUE_BOUND
    
    random.seed(nodeID)
    rValue = int(COLOR_VALUE_BOUND*random.random())
    gValue = int(COLOR_VALUE_BOUND*random.random())
    bValue = int(COLOR_VALUE_BOUND*random.random())
    
    # revert to timestamp seed
    random.seed()
    
    return [rValue, gValue, bValue]

def generate_random_graph(numberOfNodes):

    global pConnection
    
    # g denotes gephi
    global G_LAYOUT
    global G_LAYOUT_ITERATIONS
    global gNodeSize
    
    # generate random graph

    # create nodes
    for i in range(numberOfNodes):
        node = g.addNode()
        node.size = gNodeSize
        node.Label = node.Id
                                    
    connected = []
    nodeList = (list)(g.nodes)
    connected.append(nodeList[0])
    for u in g.nodes:
        if(u in connected):
            continue
        v = random.choice(connected)
        g.addEdge(u,v)
        connected.append(u)
        if(len(connected) > NUMBEROFNODES * THRESHOLD):
            for w in g.nodes:
                if(random.random() < pConnection and not w in connected):
                    g.addEdge(u,w)

    # run graph layout
    run_layout(G_LAYOUT, iters = G_LAYOUT_ITERATIONS)

def generate_linked_list():

    global NUMBEROFNODES
    global pConnection
    
    # g denotes gephi
    global G_LAYOUT
    global G_LAYOUT_ITERATIONS
    global gNodeSize
    
    # generate random graph

    # create nodes
    for i in range(NUMBEROFNODES):
        node = g.addNode()
        node.size = gNodeSize
        node.Label = node.Id
                                    
    u = (list)(g.nodes)[0]
    for v in g.nodes:
        if u == v:
            continue
        g.addEdge(u,v)
        u = v

    # run graph layout
    run_layout(G_LAYOUT, iters = G_LAYOUT_ITERATIONS)

def map_graph():
 
    global pRumor
    global colorList
    global RUMOR_LOWER_BOUND
    global RUMOR_LOWER_BOUND
 
    # map generated graph to our graph model
    allRumors = set()
    vertices = []
    
    for node in g.nodes:

        nodeRumorSet = set()
        
        pNodeRumor = random.uniform(0,1)                                        
                                    # random number between 0 and 1
        if pNodeRumor < pRumor:
            value = str(random.randint(RUMOR_LOWER_BOUND, RUMOR_LOWER_BOUND))
            nodeRumor = Rumor(node.node, value)                                        
                                    # nodes have rumors at random
            nodeRumorSet.add(nodeRumor)
            allRumors.add(nodeRumor)
            
            # populate colorList accordingly
            colorList[node.node] = get_color(nodeRumor.value)
        else:
            nodeRumor = set()

        edgeListG = set()
        neighborList = list(node.neighbors)
        
        for neighbor in neighborList:                                           
                                    # map edges
            edgeListG.add(neighbor.node)

        vertex = Vertex(node.node, nodeRumorSet, edgeListG)                     
                                    # map vertices
        vertices.append(vertex)
        
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

    global gRounds, gIterations
    
    i = 0
    # til the rumors have not been spread through the entire graph
    while(not is_finished(graph.vertices)):
    
        # each vertex link to new neighbor if able
        for vertex in graph.vertices:
            u_t = vertex.get_unlinked_neighbor()
            if (not (u_t == False)):
                print str(vertex.identity) + " is linking to " + str(u_t)
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
        
        print "First PUSH"
        push_pull(graph,i,push,rPrime)
        print "First PULL"
        push_pull(graph,i,pull,rPrime)
                
        for vertex in graph.vertices:
            # R'' = v
            vertex.rDoublePrime = set()
            vertex.rDoublePrime.update(vertex.rumors)
            # clear received rumors
            vertex.received = set()
        
        print "Second PULL"
        push_pull(graph,i,pull,rDoublePrime)
        print "Second PUSH"
        push_pull(graph,i,push,rDoublePrime)
        
        for vertex in graph.vertices:
            vertex.rumors = vertex.rPrime.union(vertex.rDoublePrime)
            vertex.rPrime = set()
            vertex.rDoublePrime = set()
            vertex.received = set()
        
        i += 1

        gIterations = i

    for v in graph.vertices:
        # print str(v.identity) + " has rumors " + str(v.rumors)
        print "Vertex " + str(v.identity) + " has " + str(len(v.rumors)) \
        + " rumors and " + str(len(v.neighbors)) + " neighbors"
    return graph
    
################################## main ########################################

def main():
    global gRounds, gIterations, K, NUMBEROFNODES
    
    generate_random_graph(NUMBEROFNODES)
    # generate_linked_list()

    # map generated graph to our graph model
    [graph, allRumors] = map_graph()

    # graph.display()
    graph.draw()

    # spread all rumors
    graph = spread_rumors(graph)

    # graph.display()               #follow spreading of rumors
    graph.draw()
    
    print "....." + str(gIterations) + " iterations, rounds: " + str(gRounds)
    
########################### end of definitions #################################

main()
