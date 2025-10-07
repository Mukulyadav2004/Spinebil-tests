# Multi-Agent Architecture Search - Quick Start Guide

## What is this?

A collaborative search framework where multiple AI agents work together to find optimal configurations. Think of it as having a team of explorers searching for treasure - they explore different areas and share their discoveries!

## Quick Start

### 1. Run the basic demo
```bash
python multi_agent_search.py
```

This will search for optimal neural network configuration across 450 possibilities.

### 2. Try comprehensive examples
```bash
python examples.py
```

This runs 4 different examples:
- Neural network hyperparameter search
- Data preprocessing pipeline optimization
- Projection pursuit parameter selection
- Strategy comparison

### 3. See spinebil integration
```bash
python spinebil_integration.py
```

Shows how this can optimize projection pursuit parameters.

### 4. Run tests
```bash
python test_multi_agent_search.py
```

13 unit tests verify everything works correctly.

## How to Use It

### Basic Pattern

```python
from multi_agent_search import MultiAgentSearchCoordinator

# 1. Define what you're searching for
search_space = {
    'parameter1': [option1, option2, option3],
    'parameter2': [optionA, optionB],
    # ... more parameters
}

# 2. Define how to evaluate options
def evaluate(config):
    # Your logic here
    score = calculate_performance(config)
    return score  # Higher is better

# 3. Create the search team
coordinator = MultiAgentSearchCoordinator(
    search_space=search_space,
    evaluation_fn=evaluate,
    num_agents=4  # Number of search agents
)

# 4. Run the search
best = coordinator.search(num_iterations=100)

# 5. Use the results
print(f"Best config: {best.config}")
print(f"Best score: {best.score}")
```

## When to Use It

✅ Good for:
- Finding optimal hyperparameters
- Configuring pipelines
- Tuning system parameters
- Exploring large discrete search spaces
- When you want robust optimization

❌ Not ideal for:
- Continuous optimization (use gradient descent instead)
- Very small search spaces (just try all options)
- When evaluation is extremely expensive

## Agent Types

### RandomSearchAgent
- Explores randomly
- Good for broad coverage
- Helps avoid local optima

### GreedySearchAgent
- Exploits good findings
- Faster convergence
- Balances exploration/exploitation

### Best Practice
Mix both types! For example with 4 agents:
```python
agent_types=['random', 'greedy', 'greedy', 'greedy']
```

## Key Features

1. **Parallel Exploration**: Multiple agents search simultaneously
2. **Knowledge Sharing**: Agents communicate their best findings
3. **Flexible**: Works for any discrete search problem
4. **Efficient**: Finds good solutions without exhaustive search
5. **Robust**: Less likely to get stuck than single-agent search

## File Overview

| File | Purpose |
|------|---------|
| `multi_agent_search.py` | Core framework |
| `examples.py` | Usage examples |
| `test_multi_agent_search.py` | Unit tests |
| `spinebil_integration.py` | Spinebil-specific examples |
| `MULTI_AGENT_SEARCH.md` | Detailed documentation |

## Tips

1. **Start small**: Try 20-50 iterations first, then increase
2. **More agents**: Use 4-8 agents for best results
3. **Communication**: Share knowledge every 5-10 iterations
4. **Evaluation function**: Make sure it returns consistent scores
5. **Search space**: Keep it reasonable (< 10,000 options ideal)

## Example Results

From the demo run:
- Search space: 450 configurations
- Used: 4 agents (2 random, 2 greedy)
- Found optimal in: ~136 evaluations (30% of search space)
- Score: 0.997 (near perfect!)

## Integration with Spinebil

Perfect for optimizing:
- Projection pursuit index selection
- Tour path parameters
- Cooling schedules
- Diagnostic thresholds
- Data preprocessing pipelines

See `spinebil_integration.py` for detailed examples.

## Need Help?

1. Check `MULTI_AGENT_SEARCH.md` for detailed docs
2. Look at `examples.py` for usage patterns
3. Run `test_multi_agent_search.py` to verify setup
4. Experiment with the demo in `multi_agent_search.py`

## License

Part of the Spinebil-tests repository for GSoC 2025.
