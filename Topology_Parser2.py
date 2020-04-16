from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.recoco import Timer
from collections import defaultdict
from pox.openflow.discovery import Discovery
from pox.lib.util import dpid_to_str
import time
from datetime import datetime
from itertools import tee, izip
from matplotlib import pylab
from pylab import *
import igraph
from igraph import *
import numpy as np
import networkx as nx, igraph as ig
from random import randint
from collections import defaultdict
from itertools import tee, izip
#---------------------------------

f_link=[]           #To hold the link failure two nodes
current_path=[]     # To hold the primary shortest path between any two nodes (e.g. 2 and 33)
new_path=[]         # To hold the new sub_path (after link failure) based on one cluster/clique
membership=None     # To hold the clusters
d = defaultdict(list) #To hold the classified clusters and their nodes (e.g. ((1,[1,2]),(2,[3,4]),...) 

class parser(EventMixin):
    G = nx.Graph()
    #global f_link=[]
    #global current_path=[]

    def __init__(self):

        def startup():
            core.openflow.addListeners(self, priority = 0)
            core.openflow_discovery.addListeners(self)
        core.call_when_ready(startup, ('openflow','openflow_discovery'))
        print "init completed"
    def _handle_LinkEvent(self, event):

        l = event.link
        sw1 = l.dpid1
        sw2 = l.dpid2
        pt1 = l.port1
        pt2 = l.port2
        self.G.add_node( sw1 )
        self.G.add_node( sw2 )
        global f_link


        if event.added:
            self.G.add_edge(sw1,sw2)

        if event.removed:
            try:
                self.G.remove_edge(sw1,sw2)
                print sw1, "---", sw2, "fails"
                f_link = [sw1,sw2]
            except:
                print "remove edge error"
        try:
            #print nx.shortest_path(self.G,2,33)

             N= nx.number_of_nodes(self.G)
             print "Number of nodes", N
             E= nx.number_of_edges(self.G)
             print "Number of Edges", E

             if (N == 37) and (E == 57):

                 print "Graph is ready now :-) "
                 print "Graph nodes are: ",self.G.nodes()
                 #nx.draw(self.G, with_labels=True)
                 #plt.show()

        except:
            print "no such complete Graph yet..."
    #---------------------------------------------------------
    #---------------------------------------------------------


    def pt(self, g, membership=None):

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



    def graph(self):

        """
        Draws the Graph/Network switches ...
        """
        #---------------------------------------------------------
        N = self.G.nodes()
        global d #= defaultdict(list)
        E = self.G.number_of_edges()
        global membership
        print "The number of Nodes in this Network:", N
        print "The number of Edges in this Network:", E
        #global f_link
        #global current_path

        #plt.ion()

        #print self.G.nodes()
        #node_labels = dict([(n,d['link_to']) for n,d in self.G.nodes(data=True)])
        #nx.draw_networkx_labels(self.G, labels=node_labels)
        fig = plt.figure()
        fig.canvas.set_window_title('The ERnet Topology View')
        nx.draw_networkx(self.G)
        plt.show()

        g = ig.Graph(len(self.G), zip(*zip(*nx.to_edgelist(self.G))[:2]))
        #self.pt(g)
        cl = g.community_fastgreedy()
        #print cl
        membership = cl.as_clustering().membership
        print membership
        self.pt(g, membership)
        #print g.get_all_shortest_paths (2, 33)
        membership.pop(0)
        for q, a in zip(N, membership):
            print 'The Node {0} --> Belongs to cluster {1}.'.format(q, a)

        #The following procedure is to get the exact nodes of each cluster, (Classification)
        for i in range (max(membership)):
            i+=1
            for j in range (len(N)):
                if membership[j]==i:
                    d[i].append(N[j])
        print "The Classified Clusters/Cliques: ", d.items()

        #Test the subgraphs correctness, which is the clusters
        #fig = plt.figure()
        #fig.canvas.set_window_title('Sub-Graph/Clique 1 of ERnet')

        #G1 = self.G.subgraph(d[1]) #each index in dictionary "d" is considered as a one cluster/subgraph of G
        #nx.draw_networkx(G1)
        #plt.show()

        #---------------------------------------------------------

        #---------------------------------------------------------
    #Function to find the shortest path and/or detect the effected path in which cluster/clique 

    def Path(self):

        N = self.G.nodes()
        E = self.G.number_of_edges()
        global f_link
        global current_path
        global membership
        global d
        pointer=0
        global new_path

        source = input("What's your source? ")
        print "The source node is ", source
        dest = input("What's your destination? ")
        print "The destination node is ", dest

        #First case: which means that the all links and nodes are fine,
        #thus, we compute the path from End-to-End based on the whole Graph G
        if (len(N) == 37) and (E == 57): #ERnet topology
            print "All Links are working fine, there is no failure at the moment"
            current_path= nx.shortest_path(self.G, source, dest)
            print "The shortest path from", source, "To ", dest, "is ", current_path
        #Second case: Which means that there is a link failure,
        #thus, we will detect the link failure belongs to which clique/cluster and then compute the new path based on that Clique 
        if (len(f_link) !=0) and ( f_link[0] and f_link[1] in current_path):
            print "Current path is suffeing from link failure"

            for nod, cliq in zip(f_link, membership):
                print 'The Node {0} --> Belongs to cluster {1}.'.format(nod, cliq)

            print "Clusters: ", d.items()
            print "The length of d is ", len(d)
            print "The first node in the failure set is ", f_link[0]
            print "The second node in the failure set is ", f_link[1]

            for i in range (len(d)):
                j=i+1
                if (f_link[0] in d[j]) and (f_link[1] in d[j]):
                    print "The link failure lies in cluster/clique", j
                    pointer=j  #To holds the effected cluter id

            #To show the effected cluster and how it looks like after the link failure
            fig = plt.figure()
            fig.canvas.set_window_title('The effected Clique of partitioned ERnet')

            F_G = self.G.subgraph(d[pointer]) #each index in dictionary "d" is considered as a one cluster/subgraph of G
            nx.draw_networkx(F_G)
            plt.show()
            new_path = nx.shortest_path(F_G, f_link[0], f_link[1])  #Apply Dijkstra on the effected Cluster only
            print "The new path is ", new_path

            #-----------------------------------------------------------------------

def launch():
    core.registerNew(parser)
