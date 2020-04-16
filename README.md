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

### Network topology: 
The network is modelled as an undirected graph G(V,E), hence, we utilised the NetworkX tool, https://networkx.github.io/, (version 1.11). In this demonstration, we provide as an example the European Reference network (ERnet) to represent the data plane topology. However, we provide three Brite simulated topologies that we generated via Waxman model.
 <div class="container">
  <div class="subcontainer">
    <figure>
      <p align="center">
<img  src= "https://user-images.githubusercontent.com/12594727/79400322-d20e1800-7f7d-11ea-9a51-dcb4d625e2d8.png"
     width="500" height="400"/>
        <figcaption><p align="center">Fig.2: Running community detection on the European Reference network topology (ERnet)
yields five communities. Colours followed by pairs of integers 
denote the names of the communities and the number of inter and intra community links. For example the red community has 4 inter community links and 7 intra-community links, Red (4,7).
The remaining communities are summarized: Blue (5,9), Green (4,8), Orange (8,10) and Yellow (4,6).</figcaption>
    </figure>
  </div>
</div>
