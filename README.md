GSoC 2025:    spinebil: Package to provide diagnostics for projection pursuit

This repository contains my submissions for hard task for the "spinebil: Package to provide diagnostics for projection pursuit" project under Google Summer of Code 2025.


Task Submission:

Hard Task Implementation

Stringy Index Simulation
This repository provides a simulation to explore the minimum and maximum values observed for various 2D patterns using the stringy index from the tourr package. The stringy index measures the linear structure of data based on PCA eigenvalues.

Overview
-The goal of this project is to understand the behavior and range of the stringy index for different data patterns. The simulation:

-Creates a custom stringy index function based on PCA eigenvalues.
-Tests this function against five distinct 2D patterns:
    Uniform noise
    Clustered data
    Linear data with noise
    Perfect linear data
    Circular data
-Reports the expected theoretical range (0.5 to 1.0) and validates this through simulation.

Usage
To run the simulation:

1.)Ensure you have R installed on your system.
2.)Install the required packages by running:

```
install.packages("tourr")
```

Results
The simulation results indicate that the stringy index ranges from 0.5 to 1.0, corresponding to the following patterns:

- Perfect line: 1.0 (all variance in one direction)
- Linear with noise: ~0.9 (most variance in one direction)
- Clustered data: ~0.6-0.7 (depends on the orientation of clusters)
- Circle/uniform noise: ~0.5 (equal variance in all directions)

These findings align with theoretical expectations and demonstrate the effectiveness of the stringy index in quantifying linear structures in data.



