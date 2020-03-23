# Python physics simulation
Python module and example to simulate basic physics 

`particles.py` is the custom core module containing the math

Based off the tutorial by Peter Collingridge: www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/ 

## Star formation

![](starformation_example_run.gif)

`starformation.py` uses the move, attract and combine functions from `particles.py` to simulate the movement and interaction of celestial bodies in space. Different bodies are generated with random mass, velocity and heading. Gravity can be observed acting between the bodies due to sufficiently large masses.

The following user controls have been implemented:
* **t** – toggle tracers
* **space** – pause/play simulation
* **↑ ↓ ← ↑** – move window view
* **-** – zoom out
* **+** – zoom in
* **r** – reset window view
