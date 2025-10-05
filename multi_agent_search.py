"""
Multi-Agent Architecture Search Framework

This module implements a multi-agent architecture search system where multiple
agents collaborate to search for optimal architectures or configurations.
"""

import random
from typing import List, Dict, Any, Callable, Optional
from abc import ABC, abstractmethod
import json


class Architecture:
    """Represents a candidate architecture or configuration."""
    
    def __init__(self, config: Dict[str, Any], score: Optional[float] = None):
        """
        Initialize an architecture.
        
        Args:
            config: Dictionary containing architecture configuration
            score: Optional fitness/performance score
        """
        self.config = config
        self.score = score
        self.id = hash(json.dumps(config, sort_keys=True))
    
    def __repr__(self):
        return f"Architecture(config={self.config}, score={self.score})"
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __hash__(self):
        return self.id


class Agent(ABC):
    """Abstract base class for search agents."""
    
    def __init__(self, agent_id: int, search_space: Dict[str, List[Any]]):
        """
        Initialize an agent.
        
        Args:
            agent_id: Unique identifier for the agent
            search_space: Dictionary defining the search space
        """
        self.agent_id = agent_id
        self.search_space = search_space
        self.best_architecture = None
        self.history = []
    
    @abstractmethod
    def propose_architecture(self) -> Architecture:
        """Propose a new architecture to evaluate."""
        pass
    
    @abstractmethod
    def update(self, architecture: Architecture, score: float):
        """
        Update agent's knowledge based on evaluated architecture.
        
        Args:
            architecture: The evaluated architecture
            score: Performance score of the architecture
        """
        pass
    
    def share_knowledge(self, other_agent: 'Agent'):
        """
        Share knowledge with another agent.
        
        Args:
            other_agent: Another agent to share knowledge with
        """
        if self.best_architecture and other_agent.best_architecture:
            if self.best_architecture.score > other_agent.best_architecture.score:
                other_agent.best_architecture = self.best_architecture


class RandomSearchAgent(Agent):
    """Agent that performs random search within the search space."""
    
    def propose_architecture(self) -> Architecture:
        """Generate a random architecture from the search space."""
        config = {}
        for key, values in self.search_space.items():
            config[key] = random.choice(values)
        return Architecture(config)
    
    def update(self, architecture: Architecture, score: float):
        """Update the agent with new evaluation results."""
        architecture.score = score
        self.history.append(architecture)
        
        if self.best_architecture is None or score > self.best_architecture.score:
            self.best_architecture = architecture


class GreedySearchAgent(Agent):
    """Agent that performs greedy search by exploiting best configurations."""
    
    def __init__(self, agent_id: int, search_space: Dict[str, List[Any]]):
        super().__init__(agent_id, search_space)
        self.exploration_rate = 0.3  # Probability of random exploration
    
    def propose_architecture(self) -> Architecture:
        """Generate architecture based on best known configuration."""
        if self.best_architecture is None or random.random() < self.exploration_rate:
            # Explore: random configuration
            config = {}
            for key, values in self.search_space.items():
                config[key] = random.choice(values)
        else:
            # Exploit: modify best configuration slightly
            config = self.best_architecture.config.copy()
            # Mutate one random parameter
            key_to_mutate = random.choice(list(self.search_space.keys()))
            config[key_to_mutate] = random.choice(self.search_space[key_to_mutate])
        
        return Architecture(config)
    
    def update(self, architecture: Architecture, score: float):
        """Update the agent with new evaluation results."""
        architecture.score = score
        self.history.append(architecture)
        
        if self.best_architecture is None or score > self.best_architecture.score:
            self.best_architecture = architecture


class MultiAgentSearchCoordinator:
    """Coordinates multiple agents in architecture search."""
    
    def __init__(
        self,
        search_space: Dict[str, List[Any]],
        evaluation_fn: Callable[[Dict[str, Any]], float],
        num_agents: int = 4,
        agent_types: Optional[List[str]] = None
    ):
        """
        Initialize the coordinator.
        
        Args:
            search_space: Dictionary defining the search space
            evaluation_fn: Function to evaluate architecture performance
            num_agents: Number of agents to use
            agent_types: List of agent type names ('random' or 'greedy')
        """
        self.search_space = search_space
        self.evaluation_fn = evaluation_fn
        self.num_agents = num_agents
        
        # Initialize agents
        self.agents = []
        if agent_types is None:
            agent_types = ['random', 'greedy'] * (num_agents // 2)
            if num_agents % 2:
                agent_types.append('random')
        
        for i in range(num_agents):
            agent_type = agent_types[i] if i < len(agent_types) else 'random'
            if agent_type == 'greedy':
                agent = GreedySearchAgent(i, search_space)
            else:
                agent = RandomSearchAgent(i, search_space)
            self.agents.append(agent)
        
        self.best_architecture = None
        self.evaluated_architectures = set()
        self.iteration = 0
    
    def search(
        self,
        num_iterations: int = 100,
        communication_interval: int = 10,
        verbose: bool = True
    ) -> Architecture:
        """
        Run the multi-agent search process.
        
        Args:
            num_iterations: Number of search iterations
            communication_interval: How often agents share knowledge
            verbose: Whether to print progress
        
        Returns:
            Best architecture found
        """
        for iteration in range(num_iterations):
            self.iteration = iteration
            
            # Each agent proposes and evaluates an architecture
            for agent in self.agents:
                architecture = agent.propose_architecture()
                
                # Skip if already evaluated
                if architecture.id in self.evaluated_architectures:
                    continue
                
                # Evaluate architecture
                score = self.evaluation_fn(architecture.config)
                agent.update(architecture, score)
                self.evaluated_architectures.add(architecture.id)
                
                # Update global best
                if self.best_architecture is None or score > self.best_architecture.score:
                    self.best_architecture = architecture
                    if verbose:
                        print(f"Iteration {iteration}, Agent {agent.agent_id}: "
                              f"New best architecture with score {score:.4f}")
            
            # Agents share knowledge periodically
            if (iteration + 1) % communication_interval == 0:
                self._facilitate_communication()
                if verbose:
                    print(f"Iteration {iteration}: Agents shared knowledge. "
                          f"Best score: {self.best_architecture.score:.4f}")
        
        return self.best_architecture
    
    def _facilitate_communication(self):
        """Facilitate knowledge sharing between agents."""
        # Each agent shares with a random subset of other agents
        for agent in self.agents:
            num_connections = random.randint(1, len(self.agents) - 1)
            other_agents = random.sample(
                [a for a in self.agents if a != agent],
                num_connections
            )
            for other_agent in other_agents:
                agent.share_knowledge(other_agent)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get search statistics."""
        agent_best_scores = [
            agent.best_architecture.score if agent.best_architecture else 0
            for agent in self.agents
        ]
        
        return {
            'best_score': self.best_architecture.score if self.best_architecture else None,
            'best_config': self.best_architecture.config if self.best_architecture else None,
            'num_evaluated': len(self.evaluated_architectures),
            'agent_best_scores': agent_best_scores,
            'iterations': self.iteration + 1
        }


def example_evaluation_function(config: Dict[str, Any]) -> float:
    """
    Example evaluation function for demonstration.
    
    This simulates evaluating a neural network architecture where:
    - Deeper networks generally perform better
    - Wider layers help up to a point
    - Optimal learning rate is around 0.01
    
    Args:
        config: Architecture configuration
    
    Returns:
        Simulated performance score (0-1)
    """
    num_layers = config.get('num_layers', 1)
    layer_size = config.get('layer_size', 32)
    learning_rate = config.get('learning_rate', 0.01)
    activation = config.get('activation', 'relu')
    
    # Simulate performance based on configuration
    score = 0.5
    
    # Deeper is generally better, but with diminishing returns
    score += min(num_layers * 0.05, 0.2)
    
    # Wider layers help
    score += min(layer_size / 512, 0.15)
    
    # Optimal learning rate
    lr_penalty = abs(learning_rate - 0.01) * 10
    score -= min(lr_penalty, 0.2)
    
    # Activation function preference
    if activation == 'relu':
        score += 0.1
    elif activation == 'tanh':
        score += 0.05
    
    # Add some random noise
    score += random.uniform(-0.05, 0.05)
    
    return max(0, min(1, score))


if __name__ == "__main__":
    # Define search space
    search_space = {
        'num_layers': [1, 2, 3, 4, 5, 6],
        'layer_size': [32, 64, 128, 256, 512],
        'learning_rate': [0.001, 0.005, 0.01, 0.05, 0.1],
        'activation': ['relu', 'tanh', 'sigmoid']
    }
    
    # Create coordinator with multiple agents
    coordinator = MultiAgentSearchCoordinator(
        search_space=search_space,
        evaluation_fn=example_evaluation_function,
        num_agents=4,
        agent_types=['random', 'greedy', 'random', 'greedy']
    )
    
    # Run search
    print("Starting multi-agent architecture search...")
    print(f"Search space size: {6 * 5 * 5 * 3} = 450 possible configurations")
    print(f"Using {coordinator.num_agents} agents\n")
    
    best = coordinator.search(num_iterations=50, communication_interval=10)
    
    # Print results
    print("\n" + "="*60)
    print("Search completed!")
    print("="*60)
    stats = coordinator.get_statistics()
    print(f"\nBest architecture found:")
    print(f"  Configuration: {best.config}")
    print(f"  Score: {best.score:.4f}")
    print(f"\nTotal architectures evaluated: {stats['num_evaluated']}")
    print(f"Agent best scores: {[f'{s:.4f}' for s in stats['agent_best_scores']]}")
