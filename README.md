# Graphical Abstract

<div class="container">
  <div class="subcontainer">
    <figure>
      <p align="center">
      <img  src="https://user-images.githubusercontent.com/12594727/81291894-90dfc400-9062-11ea-8273-49380d922d2b.png" width="700" height="700"/>
      <figcaption><p align="center">This Project was funded by the Science Foundation Ireland (SFI), https://www.sfi.ie/. </figcaption>
    </figure>
  </div>
</div>

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
      <img  src="https://user-images.githubusercontent.com/12594727/79400752-fdddcd80-7f7e-11ea-89eb-e6bd8b49ccac.png" width="450" height="120"/>
      <figcaption><p align="center">Fig.2: Path anatomy shows the rm as a middle router between the source, rs, and the destination, rd, routers.</figcaption>
    </figure>
  </div>
</div>

### Community detection: 
By dividing the network into N number of communities, we make the assumption that when a link failure event occurs, only one community will suffer from that particular failure. Therefore, the controller will need to update the only routers located in the affected community.

<div class="container">
  <div class="subcontainer">
    <figure>
      <p align="center">
      <img  src="https://user-images.githubusercontent.com/12594727/79401131-2914ec80-7f80-11ea-8435-662617e618d1.png" width="450" height="160"/>
      <figcaption><p align="center">Fig.2: Illustration of community detection and graph partitioning process: A good solution (RHS) has a high number of links between members of the same community and a low number of links to other communities..</figcaption>
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

### Requirements:
You will need to install the following:
- Mininet emulator
- POX controller
- NetworkX V.1.11
- FNSS simulator: https://fnss.github.io/ in order to convert Brite topologies into Mininet.
- igraph

![#f03c15](https://placehold.it/15/f03c15/000000?text=+) `If you use this framework or any of its code in your work then, please cite the following publication: "Rapid Restoration Techniques for Software-Defined Networks".` <br>
`@article{malik2020rapid,` <br>
`title={Rapid restoration techniques for software-defined networks},` <br>
`author={Malik, Ali and de Frein, Ruiri and Aziz, Benjamin},` <br>
`journal={Applied Sciences},` <br>
`year={2020},`<br>
`publisher={Multidisciplinary Digital Publishing Institute}}` <br>
 (https://www.mdpi.com/2076-3417/10/10/3411)
