"""
Example usage of the Multi-Agent Architecture Search framework
for different scenarios.
"""

from multi_agent_search import (
    MultiAgentSearchCoordinator,
    Architecture
)
import random


def example_1_neural_network_search():
    """Example 1: Neural Network Hyperparameter Search"""
    print("="*70)
    print("Example 1: Neural Network Hyperparameter Search")
    print("="*70 + "\n")
    
    # Define search space for neural network
    search_space = {
        'num_layers': [2, 3, 4, 5],
        'layer_size': [64, 128, 256],
        'dropout': [0.0, 0.1, 0.2, 0.3],
        'learning_rate': [0.001, 0.01, 0.1],
        'optimizer': ['adam', 'sgd', 'rmsprop']
    }
    
    def evaluate_nn_config(config):
        """Simulate neural network training performance"""
        score = 0.6
        
        # Deeper networks help
        score += config['num_layers'] * 0.03
        
        # Medium layer size is best
        if config['layer_size'] == 128:
            score += 0.1
        elif config['layer_size'] == 256:
            score += 0.05
        
        # Some dropout helps
        if 0.1 <= config['dropout'] <= 0.2:
            score += 0.08
        
        # Learning rate preference
        if config['learning_rate'] == 0.01:
            score += 0.1
        
        # Optimizer preference
        if config['optimizer'] == 'adam':
            score += 0.08
        
        # Add noise
        score += random.uniform(-0.03, 0.03)
        
        return max(0, min(1, score))
    
    # Run search
    coordinator = MultiAgentSearchCoordinator(
        search_space=search_space,
        evaluation_fn=evaluate_nn_config,
        num_agents=6
    )
    
    best = coordinator.search(num_iterations=30, communication_interval=5, verbose=False)
    
    print(f"Best Configuration Found:")
    for key, value in best.config.items():
        print(f"  {key}: {value}")
    print(f"  Score: {best.score:.4f}\n")
    
    stats = coordinator.get_statistics()
    print(f"Total evaluations: {stats['num_evaluated']}")
    print(f"Search space size: {4 * 3 * 4 * 3 * 3} configurations\n")


def example_2_data_preprocessing_pipeline():
    """Example 2: Data Preprocessing Pipeline Optimization"""
    print("="*70)
    print("Example 2: Data Preprocessing Pipeline Optimization")
    print("="*70 + "\n")
    
    # Define search space for preprocessing pipeline
    search_space = {
        'scaling': ['standard', 'minmax', 'robust', 'none'],
        'feature_selection': ['variance', 'correlation', 'mutual_info', 'none'],
        'dimensionality_reduction': ['pca', 'ica', 'lda', 'none'],
        'n_components': [5, 10, 20, 30],
        'handle_outliers': ['clip', 'remove', 'keep']
    }
    
    def evaluate_pipeline(config):
        """Simulate preprocessing pipeline performance"""
        score = 0.5
        
        # Scaling helps
        if config['scaling'] in ['standard', 'robust']:
            score += 0.12
        
        # Feature selection helps
        if config['feature_selection'] != 'none':
            score += 0.1
        
        # Dimensionality reduction can help
        if config['dimensionality_reduction'] in ['pca', 'ica']:
            score += 0.08
            # Optimal number of components
            if config['n_components'] in [10, 20]:
                score += 0.05
        
        # Outlier handling
        if config['handle_outliers'] in ['clip', 'remove']:
            score += 0.08
        
        # Add noise
        score += random.uniform(-0.04, 0.04)
        
        return max(0, min(1, score))
    
    # Run search with mixed agents
    coordinator = MultiAgentSearchCoordinator(
        search_space=search_space,
        evaluation_fn=evaluate_pipeline,
        num_agents=4,
        agent_types=['random', 'greedy', 'greedy', 'greedy']
    )
    
    best = coordinator.search(num_iterations=40, communication_interval=8, verbose=False)
    
    print(f"Best Pipeline Configuration:")
    for key, value in best.config.items():
        print(f"  {key}: {value}")
    print(f"  Score: {best.score:.4f}\n")
    
    stats = coordinator.get_statistics()
    print(f"Total evaluations: {stats['num_evaluated']}")
    print(f"Search space size: {4 * 4 * 4 * 4 * 3} configurations\n")


def example_3_projection_pursuit_indices():
    """Example 3: Projection Pursuit Index Selection (Spinebil-related)"""
    print("="*70)
    print("Example 3: Projection Pursuit Index Selection")
    print("="*70 + "\n")
    
    # Search space for projection pursuit parameters
    search_space = {
        'index_type': ['holes', 'central_mass', 'lda', 'pda', 'stringy'],
        'alpha': [0.1, 0.25, 0.5, 0.75, 1.0],
        'lambda_param': [0.0, 0.5, 1.0, 2.0],
        'cooling': ['linear', 'exponential', 'geometric'],
        'max_tries': [5, 10, 25, 50]
    }
    
    def evaluate_pp_config(config):
        """Simulate projection pursuit index performance"""
        score = 0.5
        
        # Index type effectiveness
        index_scores = {
            'holes': 0.15,
            'central_mass': 0.12,
            'lda': 0.10,
            'pda': 0.08,
            'stringy': 0.14
        }
        score += index_scores.get(config['index_type'], 0.05)
        
        # Alpha parameter
        if 0.25 <= config['alpha'] <= 0.75:
            score += 0.1
        
        # Lambda parameter
        if 0.5 <= config['lambda_param'] <= 1.0:
            score += 0.08
        
        # Cooling schedule
        if config['cooling'] == 'exponential':
            score += 0.1
        elif config['cooling'] == 'geometric':
            score += 0.08
        
        # Max tries
        if config['max_tries'] >= 25:
            score += 0.08
        
        # Add noise
        score += random.uniform(-0.03, 0.03)
        
        return max(0, min(1, score))
    
    # Run search
    coordinator = MultiAgentSearchCoordinator(
        search_space=search_space,
        evaluation_fn=evaluate_pp_config,
        num_agents=5,
        agent_types=['random', 'random', 'greedy', 'greedy', 'greedy']
    )
    
    best = coordinator.search(num_iterations=50, communication_interval=10, verbose=False)
    
    print(f"Best Projection Pursuit Configuration:")
    for key, value in best.config.items():
        print(f"  {key}: {value}")
    print(f"  Score: {best.score:.4f}\n")
    
    stats = coordinator.get_statistics()
    print(f"Total evaluations: {stats['num_evaluated']}")
    print(f"Search space size: {5 * 5 * 4 * 3 * 4} configurations\n")


def compare_agent_strategies():
    """Compare different agent strategies"""
    print("="*70)
    print("Comparison: Random vs Greedy vs Mixed Strategies")
    print("="*70 + "\n")
    
    # Simple search space
    search_space = {
        'param_a': [1, 2, 3, 4, 5],
        'param_b': [10, 20, 30, 40, 50],
        'param_c': ['x', 'y', 'z']
    }
    
    def simple_eval(config):
        """Simple evaluation with known optimal"""
        score = 0.0
        if config['param_a'] == 4:
            score += 0.4
        if config['param_b'] == 30:
            score += 0.4
        if config['param_c'] == 'y':
            score += 0.2
        return score + random.uniform(-0.05, 0.05)
    
    strategies = [
        (['random'] * 4, "All Random"),
        (['greedy'] * 4, "All Greedy"),
        (['random', 'greedy'] * 2, "Mixed")
    ]
    
    for agent_types, strategy_name in strategies:
        coordinator = MultiAgentSearchCoordinator(
            search_space=search_space,
            evaluation_fn=simple_eval,
            num_agents=4,
            agent_types=agent_types
        )
        
        best = coordinator.search(num_iterations=20, communication_interval=5, verbose=False)
        stats = coordinator.get_statistics()
        
        print(f"{strategy_name} Strategy:")
        print(f"  Best score: {best.score:.4f}")
        print(f"  Evaluations: {stats['num_evaluated']}")
        print(f"  Best config: {best.config}\n")


if __name__ == "__main__":
    # Run all examples
    example_1_neural_network_search()
    print("\n")
    
    example_2_data_preprocessing_pipeline()
    print("\n")
    
    example_3_projection_pursuit_indices()
    print("\n")
    
    compare_agent_strategies()
    
    print("="*70)
    print("All examples completed!")
    print("="*70)
