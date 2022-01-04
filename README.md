# Stewart Platform Inverse Kinematics Simulation with stochastic JONSWAP waves

<p align="center">
    <img src="misc/gifs/platform_animate.gif" width="300" height="300" />
</p>

## Prerequisite
In order to plot and animate the platform simulation points, the Python package **matplotlib** is required.

* Pip install for Python3:

      pip3 install matplotlib

## Running the default simulation

simply execute the file: **main.py**

## Applied theory

#### Wave theory
The wave elevation at time, t, at distance from calculation origin, x, is calculated with the following equations
from **DNVGL-CG-0130**

<p align="center">
    <img src="misc/figures/eq_1.PNG"  />
</p>
<p align="center">
    <img src="misc/figures/eq_2.PNG"  />
</p>
<p align="center">
    <img src="misc/figures/eq_3.PNG"  />
</p>
<p align="center">
    <img src="misc/figures/eq_4.PNG"  />
</p>

A "raft in slow waves" assumption is made when calculating the 6 degree of freedom body
displacement's amplitudes and phase lags. 

