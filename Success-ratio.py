import csv                                                             
#import networkx as nx
from operator import itemgetter
import matplotlib.pyplot as plt
import igraph 
from igraph import *
import numpy as np
from random import randint
import networkx as nx, igraph as ig
import pylab as plt 
from collections import Counter
import fnss
import random
from itertools import tee, izip
from collections import defaultdict
import string
from networkx.algorithms import community

#Modularity of ERnet = 0.533
G = nx.Graph()
#The Germany 50 Topology 
G.add_edges_from([ (1,2),(1,5),(1,4),(3,5),(3,13),(3,20),(12,14),(10,12),(10,8),(7,10),
(10,11),(7,9),(2,3),(4,3),(5,7),(5,6),(6,8),(6,13),(13,15),(13,16),(13,12),(15,14),
(14,37),(20,19),(20,21),(16,19),(16,17),(19,18),(21,18),(18,17),(17,34),(17,15),(37,11),
(37,34),(11,9),(11,29),(9,25),(9,26),(9,28),(28,29),(28,30),(29,31),(31,32),(31,34),
(31,35),(34,36),(36,35),(35,33),(33,32),(32,30),(30,27),(27,26),(26,23),(23,22),(23,24),(22,25),(25,24)])

#import community
# Read in the nodelist file
'''
with open('quakers_nodelist.csv', 'r') as nodecsv:                 
    nodereader = csv.reader(nodecsv)                                       
    nodes = [n for n in nodereader][1:]                                    

# Get a list of just the node names (the first item in each row)
node_names = [n[0] for n in nodes]                                       
'''

'''
# Read in the edgelist file
with open('xyz.csv', 'r') as edgecsv:                         
    edgereader = csv.reader(edgecsv)                                   
    edges = [tuple(e) for e in edgereader][1:]                         

# Print the number of nodes and edges in our two lists
#print(len(node_names))  
print(len(edges))                                                                               
'''

 # Initialize a undirected Graph object or use --> net.DiGraph for directed graph                                                       
#G.add_nodes_from(node_names) # Add nodes to the Graph                             
#G.add_edges_from(edges) # Add edges to the Graph  
print(nx.info(G)) # Print information about the Graph  
#print G.edges()


print "The diameter is: ", nx.diameter(G, e=None)
print "The density is: ", nx.density(G)
print "the average shortest path:", nx.average_shortest_path_length(G)

#--------------------The Longest Shortest Path --------------------------------
#Procedure to find the longest shortest path in any given topology 
Nodes= G.nodes()
G2 = nx.convert_node_labels_to_integers(G, first_label=1, ordering='default', label_attribute=None)
ns= nx.number_of_nodes(G2)
es= nx.number_of_edges(G2)
length = nx.all_pairs_shortest_path_length(G2)
x= ns # nodes in topology
#x= len(G.nodes())
y= x
Large_length = 0
Largest_P=[]
for i in range (x):
    k=i+1
    for j in range (y):
        z=j+1
        if length [k][z] > Large_length:
            Large_length = length [k][z]
            #print "The length between", k , "&", z , "is :", Large_length
            Largest_P= nx.dijkstra_path(G2, k, z)
            L_P = nx.dijkstra_path(G, Nodes[k-1], Nodes[z-1])
            #print " "
    

print "The longest_shortest_path in this topology is : ", Largest_P
print" "
print "Test1 : ",L_P
#------------------------------------------------------------------------------
print 'The length of the largest path is', Largest_P
print 'The lenght of the longest is:', len(Largest_P)
#-----------Find a percent --------------------------------------------------
#-----------------------------------------
def percentage(percent, whole):
  return round((percent * whole) / 100.0)
#----------------------------------------
pp = percentage(100, len(Largest_P))
print pp

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#The average shortest path lenght
#print 'the average shortest path length is:', round(nx.average_shortest_path_length(G2))
#------------------------------------------------------------------------------

#nx.draw_random(G, with_labels=True)    
#plt.show()

#Path= nx.dijkstra_path(G, "z@gh", "y@mn") 
#print "the path is", Path



#-----Test The Reachability between all the nodes in the graph-----------------

print (nx.is_connected(G))

#------------------------------------------------------------------------------
'''    ###Add Switches to Mininet ###
for i in range (379):
    print "S",i+1,"= net.addSwitch('s",i+1,"')"
'''

#------------------------------------------------------------------------------
'''
for i in range (50):
    print 'S',i+1,'= net.addSwitch( s',i+1,')'
'''
#------------------------------------------------------------------------------

'''
# Add Edges to Mininet
Edges= nx.edges(G)
for i in range (len(Edges)):
  print 'net.addLink (S',Edges[i][0], ',S', Edges[i][1],')'
'''
#------------------------------------------------------------------------------

'''
for i in range (379):
 print 'S',i+1,'.start(  [c0] )'
'''
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#--------------------Community procedure---------------------------------------
NN = G2.nodes()
d = defaultdict(list) #d is the dictionary that holds
d1 = defaultdict(list) #d is the dictionary that holds

#Cliques testing 

def _plot(g, membership=None):
    if membership is not None:
        gcopy = g.copy()
        edges = []
        edges_colors = []
        for edge in g.es():
            if membership[edge.tuple[0]] != membership[edge.tuple[1]]:
                edges.append(edge)
                edges_colors.append("gray")
            else:
                edges_colors.append("black")
        gcopy.delete_edges(edges)
        layout = gcopy.layout("kk")
        g.es["color"] = edges_colors
    else:
        layout = g.layout("kk")
        g.es["color"] = "gray"
    visual_style = {}
    visual_style["vertex_label_dist"] = 0
    visual_style["vertex_shape"] = "circle"
    visual_style["edge_color"] = g.es["color"]
    # visual_style["bbox"] = (4000, 2500)
    visual_style["vertex_size"] = 30
    visual_style["layout"] = layout
    visual_style["bbox"] = (1024, 768)
    visual_style["margin"] = 40
    
    #The below line can be used to show the weight of links if there is associated weight to links
    #visual_style["edge_label"] = g.es["weight"]
    
    for vertex in g.vs():
        vertex["label"] = vertex.index
    if membership is not None:
        colors = []
        for i in range(0, max(membership)+1):
            colors.append('%06X' % randint(0, 0xFFFFFF))
        for vertex in g.vs():
            vertex["color"] = str('#') + colors[membership[vertex.index]]
         
        visual_style["vertex_color"] = g.vs["color"]
    
    igraph.plot(g, **visual_style)


if __name__ == "__main__":
    #L=[]
    #g = igraph.Nexus.get("karate")
    #Converting the Networkx graph to igraph ERnet Topology 
    g = ig.Graph(len(G2), zip(*zip(*nx.to_edgelist(G2))[:2]))
    #g.delete_vertices(0)
    #_plot(g)
    cl = g.community_fastgreedy()
    #L = g.edge_disjoint_paths(2,3, checks=True)
    #print 'Disjoint paths between 2 and 3 are:', L
    #print cl
    membership = cl.as_clustering().membership
    print membership
    #_plot(g, membership)    
    #print g.get_all_shortest_paths (2, 33)
    membership.pop(0)
    for q, a in zip(NN, membership):
     print 'The Node {0} --> Belongs to cluster {1}.'.format(q, a)
    
    #The following procedure is to get the exact nodes of each cluster
    for i in range (max(membership)):
        i+=1
        for j in range (len(NN)):
            if membership[j]==i:
                d[i].append(NN[j])
    print d.items()
    fig = plt.figure() 
    fig.canvas.set_window_title('Ali Malik')
    #Test the subgraphs correctness, which is the clusters
    G3 = G2.subgraph(d[19]) #each index in dictionary "d" is considered as a one cluster/subgraph of G
    #nx.draw_random(G3, with_labels=True)    
    #plt.show()
    print 'The length of the dictionary is:', len(d)
    print "The modularity of membership is", g.modularity(cl.as_clustering().membership, weights=None)
    #--------------------------------------------------------------------------
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#pef = nx.algorithms.community.quality.coverage(G2, G2.subgraph(d[19]))
#print "The performance is ", pef

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

#------Test the connectivity after removing a link from a community------------

Sucess_Rate=0 #counter to measure the number of success
Fail_rate=0   #counter to measure the number of failure
for i in range(len(d)):
    GG = G2.subgraph(d[i])
    for i in GG.edges():
      print "Link",i
      #print i[0]
      #print i[1]
      print "The Link", i[0], ",",i[1], "will be removed"
      #Remove the direct link between the two nodes to check if there is another path between them
      GG.remove_edge(i[0], i[1])
      #Checker for Path existence if the direct link removal
      T= nx.has_path(GG, i[0], i[1])
      if T==True:
        #Means there is an alternative path
        Sucess_Rate+=1
        print "path still exists between the node", i[0], "and", i[1]
      if T==False:
        #Means there is no alternative path
        Fail_rate+=1
        print "Path not exist between the node", i[0], "and", i[1]
        
    
      #Return the removed link back to the graph
      print "The Link", i[0], ",",i[1], "will be added to the topology again" 
      GG.add_edge(i[0], i[1])
    
print "-------------------------------------------------------------------------------------"
print "The Number of Sucess cases is ", Sucess_Rate
print "The Number of fail cases is ", Fail_rate


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' Function that receives a path like : (A,B,C) And return pair  '
' of nodes as a link edges like : (A,B),(B,C).                  '
'                                                               '
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)
#------------------------------------------------------------------------------
#--------------------Function to return the counter value ---------------------
def xxx(List, Path = [], *args):
    global G2
    global d
    counter =0
    #print List
    for i in range (len(d)):
        GG = G2.subgraph(d[i])
        #print GG.edges()
        for i in range(len(List)):
            Bol = GG.has_edge(List[i][0], List[i][1])
            if Bol == True:
               counter+=1
               break
    return counter
#------------------------------------------------------------------------------
#-----------------Find Path With Length of any percentage ---------------------
P_len = 0
P=[]
T = True
for i in range (x):
    k=i+1
    for j in range (y):
      if T == True:
        z=j+1
        prc = percentage(30, (len(Largest_P)-1))
        if length [k][z] == prc:
            P= nx.dijkstra_path(G2, k, z)
            #print P
            list = []
            for pair in pairwise(P):
                list.append(pair) 
            #print list
            #break
            r = xxx(list,P)
            if r >= 1:
                print 'The satisfied counter is', r
                print 'The captured path is:', P
                T = False
                break
    
print "The path with", prc, " length is : ", P
#------------------------------------------------------------------------------
'''
#------Check if the path pass through different communities------------
list = []
for pair in pairwise(P):
    list.append(pair) 

print 'Before:', P, 'After;', list
#print list[3]
#print list[3][0]
#print list[3][1]
#------------------------------------------------------------------------------
#GG = G2.subgraph(d[1])
#print GG.edges()
#print GG.has_edge(list[3][0], list[3][1]) 
counter = 0
for i in range (len(d)):
    GG = G2.subgraph(d[i])
    for i in range(len(list)):
        Bol = GG.has_edge(list[i][0], list[i][1])
        if Bol == True:
            counter+=1
            break

print counter 

'''

#---------------------------------------------------------------
f_link = [12,13]
source = 14
dest = 1
Computed_P = nx.shortest_path(G2, source, dest)
#Function to find the shortest path and/or detect the effected path in which cluster/clique 
def Path():
        global G2
        global source
        global dest
        N = G2.nodes()
        E = G2.number_of_edges()
        global f_link
        global current_path
        global membership
        global d
        pointer = 0
        new_path = []

        #source = input("What's your source? ")
        #print "The source node is ", source
        #dest = input("What's your destination? ")
        #print "The destination node is ", dest

        #First case: which means that the all links and nodes are fine,
        #thus, we compute the path from End-to-End based on the whole Graph G
        if (len(N) == 37) and (E == 57):
            print "All Links are working fine, there is no failure at the moment"
            current_path= nx.shortest_path(G2, source, dest)
            print "The shortest path from", source, "To ", dest, "is ", current_path
        #Second case: Which means that there is a link failure,
        #thus, we will detect the link failure belongs to which clique/cluster and then compute the new path based on that Clique 
        G2.remove_edge (f_link[0], f_link[1])   #Make the down [Break!]
        if (len(f_link) !=0) and ( f_link[0] and f_link[1] in current_path):
            print "Current path is suffeing from link failure"

            for nod, cliq in zip(f_link, membership):
                print 'The Node {0} --> Belongs to cluster {1}.'.format(nod, cliq)

            #print "Clusters: ", d.items()
            #print "The length of d is ", len(d)
            print "The first node in the failure set is ", f_link[0]
            print "The second node in the failure set is ", f_link[1]

            for i in range (len(d)):
                j=i+1
                if (f_link[0] in d[j]) and (f_link[1] in d[j]):
                    print "The link failure lies in cluster/clique", j
                    pointer=j  #To holds the effected cluter id

            #To show the effected cluster and how it looks like after the link failure
            #fig = plt.figure()
            #fig.canvas.set_window_title('The effected Clique of partitioned ERnet')

            F_G = G2.subgraph(d[pointer]) #each index in dictionary "d" is considered as a one cluster/subgraph of G
            nx.draw_networkx(F_G)
            #plt.show()
            new_path = nx.shortest_path(F_G, f_link[0], f_link[1])  #Apply Dijkstra on the effected Cluster only
            print "The new path is ", new_path

print '_______________________________________________________'
Path()
#print nx.shortest_path(G2, source, dest)
print 'Algo.2 Path', nx.shortest_path(G2, source, dest)
print 'Algo.2 Path Cost', len(nx.shortest_path(G2, source, dest))-1
print 'Algo.2 Path Operation', len(Computed_P ) + len(nx.shortest_path(G2, source, dest))
print '_______________________________________________________'


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
print 'Algo.4'
mid_P=[]

# Finding the mid point of the Largest_P
if (len(Computed_P)%2 <>0):      # Means that the number of nodes in the "Largest_P" is odd
   mid_P.append( Computed_P[(len(Computed_P)/2)])   # We capture the center node in the path
   print "The mid point of the path is : ", mid_P
else:                                    # When the number of nodes in "Largest_P" is even
    mid_P.append(Computed_P[(len(Computed_P)/2)-1])           #Captering the first mid point
    mid_P.append( Computed_P[(len(Computed_P)/2)])           #Captering the second mid point
    print "The two mid points of the path are: ", mid_P
#------------------------------------------------------------------------------------------------------
#Procedure to compute the time of path discovery
print "-------------------------------------------------------------------------------------"   
#paths = list(nx.shortest_simple_paths(topology2, 165, 199))
#print "Hi", paths [1]

#topology2.remove_edge(10, 7)
#print nx.dijkstra_path (topology2, 10, 7)   #N-to-N
#print nx.dijkstra_path (topology2, 235, 5)   #E-to-mid
#print nx.dijkstra_path (topology2, 235, 266) #E-to-E


'''
#Link down scenario

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b) 

d2 = defaultdict(list)
i=1
for pair in pairwise(Largest_P):
     d2[i].append(pair)
     i=i+1

print d2.items()        # All Largest_P links as pairs 
L2=(random.choice(d2))  # Random selection link to let it down
L3=zip(*L2)
T=[map(int, i) for i in L3]
Link_Down= sum(T, [])
print "The link ", Link_Down, " will be down now now ... "
'''

mid_position = [item for item in range(len(Computed_P)) if Computed_P[item] == mid_P[0]]
print "The position of Mid_point is ", mid_position
LF_position = [item for item in range(len(Computed_P)) if Computed_P[item] == f_link[0]]
print "The position of first nodes of link failure is ", LF_position

#G.remove_edge (Link_Down[0], Link_Down[1])   #Make the down [Break!]
# Decision making based on the link failure distance from the Mid_point ((center node in the path))

if LF_position < mid_position:
    print " We are going to replace the path segment from Source --> Mid_point"
    print " The shortest path is : ", (nx.dijkstra_path(G2, Computed_P[0], mid_P[0]))
    

else:
    print "We are going to replace the path segment from Destination --> Mid_point"
    print " the shortest path is : ", (nx.dijkstra_path(G2, Computed_P[len(Computed_P)-1], mid_P[0]))
    
#------------------------------------------------------------------------------
print '_______________________________________________________'
#Algorithm 5
print 'Algo.5'
n_path = nx.shortest_path(G2, f_link[0], f_link[1]) 
print n_path
print 'Algo.5 Path Cost', (len(Computed_P)-2) + len (n_path)-1 
print 'Algo.5 Path Operation', 2 + len(n_path)
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


def random_link(List, Path = [], *args):
    return random.choice(list)



#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Procedure to check whether there is a path between all possible pairs in the Network Graph
# And then stote all these possible paths in the dictionary ... "d1" ...
p=[]
T=True  #indicator
R=0 #counter to be used as a dictionary key                               
#d = defaultdict(list) #d is the dictionary that holds
Nothing=0
for i in range (nx.number_of_nodes(G2)):
    k=i+1
    j=0
    for j in range (nx.number_of_nodes(G2)):
        z=j+1
        if (k==z):
            #print "It is the same node"
            Nothing+=1
        else:
            T= nx.has_path(G2, k, z)
            if T==True :           # Condition for path existence 
              p= nx.dijkstra_path(G2, k, z)
              if len(p)>2:
                #print "There is a path with length > 2,  between", k, "and", z
                d1[R].append(k)
                d1[R].append(z)
                R+=1
            #if T==False:
                #print "There is no path between", k, "and", z
        
    #print "**************Done with node", k,"********************"
print "Finish Testing"
print len(d1)
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def Path_Cost_alg3(Path1, Path2, f_link, *args):
   #return (len(Path2)-1) 
   Final_Path = []
   Path1.remove(f_link[0])
   Path1.remove(f_link[1])
   Final_Path = Path1 + Path2 
   return (len(Final_Path)-1)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

def Path_operation_alg3(Path1, Path2, f_link, *args):
    return  len(Path2) + 2
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def New_Path(f_link, *args):
        global G2
        N = G2.nodes()
        E = G2.number_of_edges()
        global membership
        global d
        pointer = 0
        new_path = []
        
        for i in range (len(d)):
                j=i+1
                if (f_link[0] in d[j]) and (f_link[1] in d[j]):
                    print "The link failure lies in cluster/clique", j
                    pointer = j  #To holds the effected cluter id

        F_G = G2.subgraph(d[pointer]) #each index in dictionary "d" is considered as one subgraph of G
        T = nx.has_path(F_G, f_link[0], f_link[1])
        if T == True :           # Condition for path existence 
           new_path = nx.shortest_path(F_G, f_link[0], f_link[1])  #Apply Dijkstra on the effected Cluster only
           return new_path
        else:
            return False
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def link_in_cluster(f_link):
    global d
    for i in range (len(d)):
                j=i+1
                if (f_link[0] in d[j]) and (f_link[1] in d[j]):
                    #print "The link failure lies in cluster/clique", j
                    return True
                else:
                    #print "The link failure lies in different cluster/clique"
                    return False
                    #pointer = j  #To holds the effected cluter id
    
#------------------------------------------------------------------------------
#    ... Average path cost/operation test ...
Bo = True
count = 0
cost = 0
cost2 = 0
Avg_Pcost = 0
Avg_P_operation = 0
Avg_cost_BF = 0
Avg_operation_BF = 0
prc = percentage(100, (len(Largest_P)-1))
iii = 0
P2 = []
#-----------------------------
'''
for i in range (len(d1)):
    if length [d1[i][0]] [d1[i][1]] == prc and Bo == True:
      count+=1
      print d1[i]#[0]
      #print d1[i][1]
      P1= nx.dijkstra_path(G2, d1[i][0], d1[i][1])
      print 'The first primary path is', P1
      list = []
      for pair in pairwise(P1):
       list.append(pair) 
      xx = random_link (list, P1)
      cc=0
      while cc < 5:  # 5 times trial to pick random link within a particular path
       if link_in_cluster(xx) == True: 
         
         print 'The random selected link is:', xx
         G2.remove_edge (xx[0], xx[1])   #Make the down [Break!]
         print 'The link', xx[0], xx[1], 'is removed'
         #P2 = New_Path(xx, P1)
         #P2= nx.dijkstra_path(G2, d1[i][0], d1[i][1])
         #print 'The new alternative path is', P2
         #cost = Path_Cost_alg2(P1, P2)
         #Avg_Pcost = Avg_Pcost + cost
         if New_Path(xx) != False:
            P2 = New_Path(xx)
            iii = iii + 1  # To record the number of succeful cases
            print "The new path is ", P2
            cost = Path_Cost_alg3(P1, P2, xx)
            Avg_Pcost = Avg_Pcost + cost
            cost2 = Path_operation_alg3(P1, P2, xx)
            Avg_P_operation = Avg_P_operation + cost2

            #To capture the max and min values
            if iii == 1:
               min_cost = cost
               min_operation = cost2
               max_cost = cost
               max_operation = cost2
            if iii > 1:
               if cost < min_cost:
                  min_cost = cost
               if cost > max_cost:
                  max_cost = cost
               if cost2 < min_operation:
                  min_operation = cost2
               if cost2 > max_operation:
                  max_operation = cost2

         #Avg_cost_BF = Avg_cost_BF + (len(P1)-1)
         #cost2 = Path_operation_alg2(P1,P2)
         #Avg_P_operation = Avg_P_operation + cost2
         #Avg_operation_BF = Avg_operation_BF + (len(P1))
         G2.add_edge(xx[0], xx[1]) 
         cc = cc + 1
         break
       else:
          #print 'We will try to pick another random link wiath a', cc, 'trial' 
          cc = cc + 1  
        
        
    if count > 500:#99:
        Bo = False
        break
print 'The number of succefull cases is', iii
Avg1 = Avg_Pcost / iii
print 'The average path cost of algorithm.3 is', round (Avg1)
Avg2 = Avg_P_operation / iii
print 'The average operation path of algorithm.3 is', round (Avg2)


print 'Min path cost is', min_cost
print 'Max path cost is', max_cost
print 'Min operation cost is', min_operation
print 'Max operation cost is', max_operation
'''
#----------------------------------------
