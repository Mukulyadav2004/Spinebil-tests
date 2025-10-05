"""
Spinebil Integration Example

This module demonstrates how the multi-agent architecture search framework
can be integrated with the spinebil package for projection pursuit optimization.

This is a conceptual example showing potential integration points.
"""

from multi_agent_search import MultiAgentSearchCoordinator
import random


def example_projection_pursuit_optimization():
    """
    Example: Using multi-agent search to optimize projection pursuit parameters
    
    In a real spinebil integration, this would:
    1. Use actual tourr package functions
    2. Evaluate real projection indices on actual data
    3. Optimize parameters for visualization quality
    """
    print("="*70)
    print("Spinebil Integration: Projection Pursuit Parameter Optimization")
    print("="*70 + "\n")
    
    # Define search space for projection pursuit
    search_space = {
        # Index selection
        'index_function': ['holes', 'central_mass', 'lda', 'pda', 'stringy'],
        
        # Tour parameters
        'tour_path': ['guided', 'little', 'grand'],
        
        # Optimization parameters
        'cooling': ['linear', 'exponential', 'geometric'],
        'max_tries': [10, 25, 50, 100],
        
        # Index-specific parameters
        'alpha': [0.1, 0.25, 0.5, 0.75, 1.0],
        'lambda': [0.0, 0.5, 1.0, 2.0],
    }
    
    def evaluate_projection_config(config):
        """
        Simulated evaluation of projection pursuit configuration.
        
        In real spinebil integration, this would:
        - Apply the configuration to actual data
        - Run projection pursuit with specified parameters
        - Calculate diagnostic metrics (structure found, tour quality, etc.)
        - Return composite score
        
        This simulation mimics realistic preferences:
        - stringy and holes indices often perform well
        - guided tour is generally effective
        - exponential cooling balances speed and quality
        - moderate alpha values work best
        """
        score = 0.5
        
        # Index function effectiveness (simulated)
        index_scores = {
            'stringy': 0.15,
            'holes': 0.14,
            'central_mass': 0.12,
            'lda': 0.10,
            'pda': 0.08
        }
        score += index_scores.get(config['index_function'], 0.05)
        
        # Tour path preference
        if config['tour_path'] == 'guided':
            score += 0.12
        elif config['tour_path'] == 'grand':
            score += 0.08
        
        # Cooling schedule
        cooling_scores = {
            'exponential': 0.10,
            'geometric': 0.08,
            'linear': 0.05
        }
        score += cooling_scores.get(config['cooling'], 0.0)
        
        # Max tries (more is better, but diminishing returns)
        if config['max_tries'] >= 50:
            score += 0.10
        elif config['max_tries'] >= 25:
            score += 0.07
        
        # Alpha parameter (moderate values best)
        if 0.25 <= config['alpha'] <= 0.75:
            score += 0.08
        
        # Lambda parameter
        if 0.5 <= config['lambda'] <= 1.0:
            score += 0.06
        
        # Add realistic noise
        score += random.uniform(-0.04, 0.04)
        
        return max(0, min(1, score))
    
    # Create multi-agent coordinator
    print("Initializing multi-agent search...")
    print(f"Search space: {5 * 3 * 3 * 4 * 5 * 4} = 3,600 possible configurations")
    print("Using 6 agents (mix of random and greedy)\n")
    
    coordinator = MultiAgentSearchCoordinator(
        search_space=search_space,
        evaluation_fn=evaluate_projection_config,
        num_agents=6,
        agent_types=['random', 'random', 'greedy', 'greedy', 'greedy', 'greedy']
    )
    
    # Run search
    print("Starting collaborative search...\n")
    best = coordinator.search(
        num_iterations=80,
        communication_interval=10,
        verbose=True
    )
    
    # Display results
    print("\n" + "="*70)
    print("Optimal Configuration Found")
    print("="*70)
    print(f"\nProjection Pursuit Parameters:")
    print(f"  Index Function: {best.config['index_function']}")
    print(f"  Tour Path: {best.config['tour_path']}")
    print(f"  Cooling: {best.config['cooling']}")
    print(f"  Max Tries: {best.config['max_tries']}")
    print(f"  Alpha: {best.config['alpha']}")
    print(f"  Lambda: {best.config['lambda']}")
    print(f"\nQuality Score: {best.score:.4f}")
    
    # Get statistics
    stats = coordinator.get_statistics()
    print(f"\nSearch Statistics:")
    print(f"  Configurations Evaluated: {stats['num_evaluated']} / 3,600")
    print(f"  Coverage: {stats['num_evaluated']/3600*100:.1f}%")
    print(f"  Agent Best Scores: {[f'{s:.4f}' for s in stats['agent_best_scores']]}")
    
    return best, coordinator


def example_diagnostic_threshold_optimization():
    """
    Example: Optimizing diagnostic thresholds for projection pursuit
    """
    print("\n\n" + "="*70)
    print("Spinebil Integration: Diagnostic Threshold Optimization")
    print("="*70 + "\n")
    
    # Search space for diagnostic thresholds
    search_space = {
        'convergence_threshold': [1e-6, 1e-5, 1e-4, 1e-3],
        'min_structure_score': [0.1, 0.2, 0.3, 0.4, 0.5],
        'outlier_percentile': [0.90, 0.95, 0.99],
        'min_projection_distance': [0.01, 0.05, 0.1, 0.2],
        'stability_window': [5, 10, 20, 30]
    }
    
    def evaluate_thresholds(config):
        """Simulated evaluation of diagnostic thresholds"""
        score = 0.5
        
        # Convergence threshold (moderate is best)
        if config['convergence_threshold'] == 1e-4:
            score += 0.15
        elif config['convergence_threshold'] == 1e-5:
            score += 0.12
        
        # Structure score (higher threshold = stricter)
        if config['min_structure_score'] >= 0.3:
            score += 0.1
        
        # Outlier detection
        if config['outlier_percentile'] == 0.95:
            score += 0.1
        
        # Projection distance
        if 0.05 <= config['min_projection_distance'] <= 0.1:
            score += 0.12
        
        # Stability window
        if 10 <= config['stability_window'] <= 20:
            score += 0.08
        
        score += random.uniform(-0.03, 0.03)
        return max(0, min(1, score))
    
    coordinator = MultiAgentSearchCoordinator(
        search_space=search_space,
        evaluation_fn=evaluate_thresholds,
        num_agents=4
    )
    
    print(f"Search space: {4 * 5 * 3 * 4 * 4} = 960 configurations")
    print("Using 4 agents\n")
    
    best = coordinator.search(num_iterations=50, communication_interval=10, verbose=False)
    
    print("Optimal Diagnostic Thresholds:")
    for key, value in best.config.items():
        print(f"  {key}: {value}")
    print(f"\nScore: {best.score:.4f}")
    
    stats = coordinator.get_statistics()
    print(f"Evaluated {stats['num_evaluated']} configurations")


def integration_benefits():
    """Print information about integration benefits"""
    print("\n\n" + "="*70)
    print("Benefits of Multi-Agent Search for Spinebil")
    print("="*70 + "\n")
    
    benefits = [
        "1. Automated Parameter Tuning:",
        "   - Find optimal projection pursuit parameters without manual tuning",
        "   - Reduce time spent on parameter selection",
        "",
        "2. Robust Optimization:",
        "   - Multiple agents explore different regions of parameter space",
        "   - Less likely to get stuck in local optima",
        "   - Knowledge sharing helps agents converge faster",
        "",
        "3. Scalability:",
        "   - Can handle large search spaces efficiently",
        "   - Parallel exploration by multiple agents",
        "   - Communicates best findings across agents",
        "",
        "4. Flexibility:",
        "   - Easy to customize search space for different use cases",
        "   - Plug in custom evaluation metrics",
        "   - Mix different agent strategies for best results",
        "",
        "5. Integration Points with Spinebil:",
        "   - Optimize projection pursuit index parameters",
        "   - Tune diagnostic thresholds",
        "   - Find best visualization parameters",
        "   - Select optimal tour paths and cooling schedules",
        "   - Configure data preprocessing pipelines",
    ]
    
    for line in benefits:
        print(line)


if __name__ == "__main__":
    # Run examples
    print("Multi-Agent Architecture Search Integration with Spinebil\n")
    print("This demonstrates how the framework can be used to optimize")
    print("projection pursuit parameters and diagnostic thresholds.\n")
    
    # Example 1: Projection pursuit optimization
    best_pp, coordinator_pp = example_projection_pursuit_optimization()
    
    # Example 2: Diagnostic threshold optimization
    example_diagnostic_threshold_optimization()
    
    # Show integration benefits
    integration_benefits()
    
    print("\n" + "="*70)
    print("Examples completed!")
    print("="*70)
