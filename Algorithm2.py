from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.recoco import Timer
from collections import defaultdict
from pox.openflow.discovery import Discovery
from pox.lib.util import dpid_to_str
from matplotlib import pylab 
from pylab import * 
import igraph 
from igraph import * 
import numpy as np 
import networkx as nx, igraph as ig 
from random import randint 
from collections import defaultdict 
from itertools import tee, izip
import time
import copy
 
log = core.getLogger()
mac_map = {}
switches = {}
myswitches=[]
adjacency = defaultdict(lambda:defaultdict(lambda:None))
ori_adjacency = defaultdict(lambda:defaultdict(lambda:None))
current_p=[]
d_bk={}
link_fail=[]
zone_member=[]
new_adjacency = defaultdict(lambda:defaultdict(lambda:None))

def minimum_distance(distance, Q):
  #print "distance=", distance
  #print "Q=", Q
  min = float('Inf')
  node = 0
  for v in Q:
    if distance[v] < min:
      min = distance[v]
      node = v
  #print "min=", min, " node=", node
  return node

def _get_raw_path (src,dst,adj):
  #Dijkstra algorithm
  print "src=",src," dst=", dst
  #print "myswitches=", myswitches
  distance = {}
  previous = {} 	
  sws = myswitches
 
  for dpid in sws:
    distance[dpid] = float('Inf')
    previous[dpid] = None
 
  distance[src]=0
  Q=set(sws)

  while len(Q)>0:
    u = minimum_distance(distance, Q)
    #print "u=", u
    Q.remove(u)
   
    for p in sws:
      if adj[u][p]!=None:
        w = 1
        if distance[u] + w < distance[p]:
          distance[p] = distance[u] + w
          previous[p] = u
  r=[]
  p=dst 
  r.append(p)
  q=previous[p]
  while q is not None:
    if q == src:
      r.append(q)
      break
    p=q
    r.append(p)
    q=previous[p] 
 
  r.reverse()  
  return r  

def _get_raw_path2 (src,dst,adj):
  #Dijkstra algorithm
  global zone_member
  print "src=",src," dst=", dst
  #print "myswitches=", myswitches
  distance = {}
  previous = {} 	
  sws = zone_member
 
  for dpid in sws:
    distance[dpid] = float('Inf')
    previous[dpid] = None
 
  distance[src]=0
  Q=set(sws)

  while len(Q)>0:
    u = minimum_distance(distance, Q)
    #print "u=", u
    Q.remove(u)
   
    for p in sws:
      if adj[u][p]!=None:
        w = 1
        if distance[u] + w < distance[p]:
          distance[p] = distance[u] + w
          previous[p] = u
  r=[]
  p=dst 
  r.append(p)
  q=previous[p]
  while q is not None:
    if q == src:
      r.append(q)
      break
    p=q
    r.append(p)
    q=previous[p] 
 
  r.reverse()  
  return r 

class Switch (EventMixin):
  def __init__ (self):
    self.connection = None
    self.ports = None
    self.dpid = None
    self._listeners = None
    self._connected_at = None
    #To test the longest shortest path in ERnet topology
    mac_map[str("00:00:00:00:00:01")]=(1,1)
    mac_map[str("00:00:00:00:00:02")]=(36,1)
  def __repr__ (self):
    return dpid_to_str(self.dpid)

  def _install2 (self, in_port, out_port, match, dpid):
    msg = of.ofp_flow_mod()
    msg.match = match
    msg.match.in_port = in_port
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.actions.append(of.ofp_action_output(port = out_port))
    switches[dpid].connection.send(msg)

  def _install (self, in_port, out_port, match, buf = None):
    msg = of.ofp_flow_mod()
    msg.match = match
    msg.match.in_port = in_port
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    msg.actions.append(of.ofp_action_output(port = out_port))
    msg.buffer_id = buf
    self.connection.send(msg)

  def _handle_PacketIn (self, event):
    global current_p, link_fail
    #print "_hanle_PacketIn() is called at", self.dpid
    packet = event.parsed
    #print "packet.src=", str(packet.src), " packet.dst=", packet.dst
    if str(packet.src) !="00:00:00:00:00:01" and str(packet.src) !="00:00:00:00:00:02":
      return   
    #print "switches=", switches
    #print "adjacency=", adjacency
    path = _get_raw_path (mac_map[str(packet.src)][0], mac_map[str(packet.dst)][0],adjacency) 
    current_p=copy.deepcopy(path)  
    print "path=", path, "current_p=", current_p
    if len(link_fail)!=0 and self.dpid in link_fail:
      print "link_fail=", link_fail, "self.dpid=", self.dpid
      if self.dpid == link_fail[0]:
        p1=_get_raw_path2(link_fail[0], link_fail[1],new_adjacency)
        p2=_get_raw_path (mac_map[str(packet.src)][0], mac_map[str(packet.dst)][0],ori_adjacency)
        print "p1=", p1, "p2=", p2 
      else:
        p1=_get_raw_path2(link_fail[1], link_fail[0],new_adjacency)
        p2=_get_raw_path (mac_map[str(packet.src)][0], mac_map[str(packet.dst)][0],ori_adjacency)
        print "p1=", p1, "p2=", p2

      indx=p2.index(p1[0])
      p1.remove(p1[0])
      #p1.remove(p1[len(p1)-1])
      j=1
      for i in p1:
          if j==len(p1):
            break
          p2.insert(indx+j,i)
          j+=1
      print "final p2=", p2, " final p1=", p1
      path=p2
      j=1
      for i in p1:
        next=path[path.index(self.dpid)+j+1]
        #print "next=", next
        output_port = adjacency[i][next]
        input_port = adjacency[path[path.index(self.dpid)+j]][path[path.index(self.dpid)+j-1]]
        #print "path[path.index(self.dpid)+j]=",path[path.index(self.dpid)+j]
        #print "path[path.index(self.dpid)+j-1]=",path[path.index(self.dpid)+j-1]
        #print "output_port=", output_port
        #print "input_port=", input_port
        match = of.ofp_match.from_packet(packet)
        self._install2(input_port, output_port, match, i)
        j+=1 
           
    if mac_map[str(packet.dst)][0]!=self.dpid:
      next=path[path.index(self.dpid)+1]
      #print "next=", next
      output_port = adjacency[self.dpid][next]
      #print "output_port=", adjacency[self.dpid][next]
      match = of.ofp_match.from_packet(packet)
      self._install(event.port, output_port, match) 
    else:
      output_port=mac_map[str(packet.dst)][1]
    msg = of.ofp_packet_out()
    msg.actions.append(of.ofp_action_output(port = output_port))
    msg.buffer_id = event.ofp.buffer_id
    msg.in_port = event.port
    self.connection.send(msg)

  def disconnect (self):
    if self.connection is not None:
      log.debug("Disconnect %s" % (self.connection,))
      self.connection.removeListeners(self._listeners)
      self.connection = None
      self._listeners = None

  def connect (self, connection):
    #print "type(conection.dpid)=", type(connection.dpid)
    if self.dpid is None:
      self.dpid = connection.dpid
    assert self.dpid == connection.dpid
    if self.ports is None:
      self.ports = connection.features.ports
    self.disconnect()
    log.debug("Connect %s" % (connection,))
    self.connection = connection
    self._listeners = self.listenTo(connection)
    self._connected_at = time.time()

  def _handle_ConnectionDown (self, event):
    self.disconnect() 

class l2_multi (EventMixin):
  G = nx.Graph()

  def __init__ (self):
    # Listen to dependencies
    def startup ():
      core.openflow.addListeners(self, priority=0)
      core.openflow_discovery.addListeners(self)
    core.call_when_ready(startup, ('openflow','openflow_discovery'))

  def _handle_ConnectionUp (self, event):
      sw = switches.get(event.dpid)
      if sw is None:
        # New switch
        sw = Switch()
        switches[event.dpid] = sw
        sw.connect(event.connection)
        myswitches.append(event.dpid)
      else:
        sw.connect(event.connection)

  def _handle_LinkEvent(self, event):
        global current_p, d_bk, link_fail, zone_member
        l = event.link 
        sw1 = l.dpid1 
        sw2 = l.dpid2 
        pt1 = l.port1 
        pt2 = l.port2 
        self.G.add_node( sw1 )
        self.G.add_node( sw2 )

        no_edges=0
        for p in myswitches:
          for q in myswitches:
             if adjacency[p][q]!=None: 
               no_edges+=1
        print "number of edges=", (no_edges*0.5)         
        print "current_p=", current_p
   
        if event.added:
            self.G.add_edge(sw1,sw2)
            #print "link is added" 
            if adjacency[sw1][sw2] is None:
              adjacency[sw1][sw2] = l.port1
              adjacency[sw2][sw1] = l.port2   
            if ori_adjacency[sw1][sw2] is None:
              ori_adjacency[sw1][sw2] = l.port1
              ori_adjacency[sw2][sw1] = l.port2  
 
        if event.removed: 
            #print "link is removed"
            print sw1, "----", sw2, " is removed"
            print "d_bk.items()=", d_bk.items() 
            zone=-1
            for i, j in d_bk.items():
              #print i, j
              if sw1 in j and sw2 in j:
                zone=i
                zone_member=j
                print "link_fail at zone:", i, "zone_member=", zone_member   
                break;
            for p in d_bk[zone]:
              for q in d_bk[zone]:
                 if adjacency[p][q] is not None or (p!=sw1 and q!=sw2) or (p!=sw2 and q!=sw1):
                   new_adjacency[p][q]=adjacency[p][q]
            print "new_adjacency=", new_adjacency
      
            link_fail=[sw1,sw2]  
            clear = of.ofp_flow_mod(command=of.OFPFC_DELETE)  
            for dpid in link_fail:
              if switches[dpid].connection is None: continue
              switches[dpid].connection.send(clear)

            try: 
                if sw2 in adjacency[sw1]: del adjacency[sw1][sw2]
                if sw1 in adjacency[sw2]: del adjacency[sw2][sw1]
                self.G.remove_edge(sw1,sw2)
            except: 
                print "remove edge error" 
        
        try:
            N = nx.number_of_nodes(self.G)
            E= nx.number_of_edges(self.G) 
            NN = self.G.nodes() 
            EE = self.G.number_of_edges()
            d = defaultdict(list) 
            print "N=", N, "E=", E             #We take ERnet as an example topology
            if (N == 37) and (E == 58): 
              print "Graph is ready now :-)"
              print "Graph nodes are:", self.G.nodes()
              g = ig.Graph(len(self.G), zip(*zip(*nx.to_edgelist(self.G))[:2])) 
              cl = g.community_fastgreedy() 
              #print cl  
              membership = cl.as_clustering().membership 
              print "membership=", membership  
              #print g.get_all_shortest_paths (2, 33) 
              membership.pop(0) 
              for q, a in zip(NN, membership): 
                print 'The Node {0} --> Belongs to cluster {1}.'.format(q, a) 
              for i in range (max(membership)): 
                i+=1 
                for j in range (len(NN)): 
                  if membership[j]==i: 
                     d[i].append(NN[j]) 
              print d.items() 
              d_bk=dict(d)
        except:
            print "no such complete Graph yet..." 
        
def launch ():
  core.registerNew(l2_multi)
