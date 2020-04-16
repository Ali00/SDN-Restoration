# SDN-Restoration

### Framework:
The framework has been evaluated by the SDN emulator "Mininet", http://mininet.org/ , with POX as a network operating system
(controller), https://github.com/noxrepo/pox/.
<div class="container">
  <div class="subcontainer">
    <figure>
      <p align="center">
      <img  src="https://user-images.githubusercontent.com/12594727/79400075-0e8d4400-7f7d-11ea-9315-b01b57f44d7c.png" width="300" height="300"/>
      <figcaption><p align="center">Fig.1: Proposed framework components: the primary contribution of this paper lies in the Community Detection and the Path Anatomy blocks. Openflow is used on the southbound interface and POX APIs are used on the northbound interface. The framework components are labelled with the algorithms that describe their function.</figcaption>
    </figure>
  </div>
</div>

### Path anatomy: 
In a path anatomy the sequence of routers that form the path can be partitioned into two sub-paths which have equal length. Recovery can be achieved by either reconfiguring the flow tables associated with the half of the path which contains the failure, or the link which has failed.
<div class="container">
  <div class="subcontainer">
    <figure>
      <p align="center">
      <img  src="https://user-images.githubusercontent.com/12594727/79400752-fdddcd80-7f7e-11ea-89eb-e6bd8b49ccac.png" width="450" height="160"/>
      <figcaption><p align="center">Fig.2: Path anatomy shows the rm as a middle router between the source, rs, and the destination, rd, routers.</figcaption>
    </figure>
  </div>
</div>

### Community detection: 

<div class="container">
  <div class="subcontainer">
    <figure>
      <p align="center">
      <img  src="https://user-images.githubusercontent.com/12594727/79401058-efdc7c80-7f7f-11ea-96f6-1c47e2d206bf.png" width="450" height="160"/>
      <figcaption><p align="center">Fig.2: Path anatomy shows the rm as a middle router between the source, rs, and the destination, rd, routers.</figcaption>
    </figure>
  </div>
</div>



### Network topology: 
The network is modelled as an undirected graph G(V,E), hence, we utilised the NetworkX tool, https://networkx.github.io/, (version 1.11). In this demonstration, we provide as an example the European Reference network (ERnet) to represent the data plane topology. However, we provide three Brite simulated topologies that we generated via Waxman model.
 <div class="container">
  <div class="subcontainer">
    <figure>
      <p align="center">
<img  src= "https://user-images.githubusercontent.com/12594727/79400322-d20e1800-7f7d-11ea-9a51-dcb4d625e2d8.png"
     width="500" height="400"/>
        <figcaption><p align="center">Fig.4: Running community detection on the European Reference network topology (ERnet)
yields five communities. Colours followed by pairs of integers 
denote the names of the communities and the number of inter and intra community links. For example the red community has 4 inter community links and 7 intra-community links, Red (4,7).
The remaining communities are summarized: Blue (5,9), Green (4,8), Orange (8,10) and Yellow (4,6).</figcaption>
    </figure>
  </div>
</div>


![#f03c15](https://placehold.it/15/f03c15/000000?text=+) `If you use this framework or any of its code in your work then, please cite the following publication: "Rapid Restoration Techniques for Software-Defined Networks".`
