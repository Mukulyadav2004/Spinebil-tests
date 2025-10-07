# Multi-Agent Architecture Search

A Python framework for collaborative architecture search using multiple agents.

## Overview

This framework implements a multi-agent system where multiple search agents work together to find optimal architectures or configurations. Each agent explores the search space independently while periodically sharing knowledge with other agents.

## Features

- **Multiple Agent Types**: 
  - `RandomSearchAgent`: Performs random exploration of the search space
  - `GreedySearchAgent`: Balances exploration and exploitation based on best known configurations
  
- **Agent Communication**: Agents periodically share their best findings with each other

- **Flexible Search Space**: Define any parameter space with discrete choices

- **Customizable Evaluation**: Plug in your own evaluation function

## Architecture

### Core Components

1. **Architecture**: Represents a candidate configuration with its score
2. **Agent**: Abstract base class for search agents
3. **MultiAgentSearchCoordinator**: Orchestrates the multi-agent search process

### Agent Types

#### RandomSearchAgent
Performs pure random search, useful for broad exploration of the search space.

#### GreedySearchAgent
Uses an epsilon-greedy strategy:
- 30% of the time: random exploration
- 70% of the time: exploit best known configuration with small mutations

## Usage

### Basic Example

```python
from multi_agent_search import MultiAgentSearchCoordinator

# Define your search space
search_space = {
    'num_layers': [1, 2, 3, 4, 5],
    'layer_size': [32, 64, 128, 256],
    'learning_rate': [0.001, 0.01, 0.1],
    'activation': ['relu', 'tanh', 'sigmoid']
}

# Define evaluation function
def evaluate_architecture(config):
    # Your evaluation logic here
    # Return a score (higher is better)
    return score

# Create coordinator
coordinator = MultiAgentSearchCoordinator(
    search_space=search_space,
    evaluation_fn=evaluate_architecture,
    num_agents=4,
    agent_types=['random', 'greedy', 'random', 'greedy']
)

# Run search
best_architecture = coordinator.search(
    num_iterations=100,
    communication_interval=10,
    verbose=True
)

print(f"Best config: {best_architecture.config}")
print(f"Best score: {best_architecture.score}")
```

### Running the Demo

The framework includes a built-in example that simulates neural network architecture search:

```bash
python multi_agent_search.py
```

This will run a search over:
- Number of layers: 1-6
- Layer sizes: 32, 64, 128, 256, 512
- Learning rates: 0.001, 0.005, 0.01, 0.05, 0.1
- Activation functions: relu, tanh, sigmoid

## Parameters

### MultiAgentSearchCoordinator

- `search_space`: Dictionary mapping parameter names to lists of possible values
- `evaluation_fn`: Function that takes a config dict and returns a score (float)
- `num_agents`: Number of agents to use in the search (default: 4)
- `agent_types`: List specifying type of each agent ('random' or 'greedy')

### search() method

- `num_iterations`: Number of search iterations to run
- `communication_interval`: How often agents share knowledge (in iterations)
- `verbose`: Whether to print progress updates

## How It Works

1. **Initialization**: Multiple agents are created, each with knowledge of the search space

2. **Search Loop**: For each iteration:
   - Each agent proposes a new architecture
   - The architecture is evaluated using the provided function
   - The agent updates its internal state based on the result
   - The global best architecture is updated if needed

3. **Communication**: At regular intervals:
   - Agents share their best findings with random subsets of other agents
   - This allows knowledge to spread through the agent network

4. **Termination**: After the specified number of iterations, return the best architecture found

## Benefits of Multi-Agent Approach

- **Parallel Exploration**: Multiple agents can explore different regions simultaneously
- **Knowledge Sharing**: Agents learn from each other's discoveries
- **Diversity**: Different agent types (random vs greedy) provide different search strategies
- **Robustness**: Less likely to get stuck in local optima compared to single-agent search

## Extension Ideas

- Add more sophisticated agent types (evolutionary, Bayesian optimization, etc.)
- Implement different communication strategies
- Add support for continuous search spaces
- Include early stopping criteria
- Add visualization of the search process

## Integration with Spinebil

This multi-agent framework can be integrated with the spinebil package for:
- Searching optimal projection pursuit indices
- Finding best transformation parameters
- Tuning visualization parameters
- Optimizing diagnostic thresholds
