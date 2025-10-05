***GSOC 2025:    spinebil: Package to provide diagnostics for projection pursuit***

**This repository contains my submissions for hard task for the "spinebil: Package to provide diagnostics for projection pursuit" project under Google Summer of Code 2025.**


*Hard Task Implementation*

## 1. Stringy Index Simulation
This repository provides a simulation to explore the minimum and maximum values observed for various 2D patterns using the stringy index from the tourr package. The stringy index measures the linear structure of data based on PCA eigenvalues.

## 2. Multi-Agent Architecture Search
A Python framework for collaborative architecture search using multiple agents. This framework can be used for hyperparameter optimization, pipeline configuration, and finding optimal projection pursuit parameters. See [MULTI_AGENT_SEARCH.md](MULTI_AGENT_SEARCH.md) for detailed documentation.


***Overview***

### Stringy Index Simulation
*The goal of this project is to understand the behavior and range of the stringy index for different data patterns. The simulation:*

    Creates a custom stringy index function based on PCA eigenvalues.
    Tests this function against five distinct 2D patterns:
        Uniform noise
        Clustered data
        Linear data with noise
        Perfect linear data
        Circular data
    Reports the expected theoretical range (0.5 to 1.0) and validates this through simulation.

### Multi-Agent Architecture Search
*A collaborative search framework where multiple agents work together to find optimal configurations:*

    Multiple agent types (Random, Greedy) with different search strategies
    Agents periodically share knowledge to accelerate convergence
    Flexible search space definition
    Customizable evaluation functions
    Examples for neural networks, data pipelines, and projection pursuit parameters

***Usage***

### Stringy Index Simulation
*To run the stringy index simulation:*

1.)Ensure you have R installed on your system.
2.)Install the required packages by running:

```
install.packages("tourr")
```

### Multi-Agent Architecture Search
*To run the multi-agent architecture search:*

1.)Ensure you have Python 3.x installed.

2.)Run the main demo:
```bash
python multi_agent_search.py
```

3.)Or run the comprehensive examples:
```bash
python examples.py
```

***Results***

### Stringy Index Simulation
*The simulation results indicate that the stringy index ranges from 0.5 to 1.0, corresponding to the following patterns:*

- Perfect line: 1.0 (all variance in one direction)
- Linear with noise: ~0.9 (most variance in one direction)
- Clustered data: ~0.6-0.7 (depends on the orientation of clusters)
- Circle/uniform noise: ~0.5 (equal variance in all directions)

These findings align with theoretical expectations and demonstrate the effectiveness of the stringy index in quantifying linear structures in data.

### Multi-Agent Architecture Search
*The framework demonstrates effective collaborative search:*

- Multiple agents explore the search space in parallel
- Knowledge sharing accelerates convergence
- Mixed strategies (random + greedy) often perform best
- Suitable for various optimization tasks (neural networks, pipelines, projection pursuit)
- Example: Finding optimal neural network configuration in 136 evaluations out of 450 possible configurations

For detailed documentation, see [MULTI_AGENT_SEARCH.md](MULTI_AGENT_SEARCH.md).

