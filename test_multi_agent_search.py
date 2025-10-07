"""
Test suite for Multi-Agent Architecture Search framework
"""

import unittest
from multi_agent_search import (
    Architecture,
    RandomSearchAgent,
    GreedySearchAgent,
    MultiAgentSearchCoordinator
)


class TestArchitecture(unittest.TestCase):
    """Test the Architecture class"""
    
    def test_architecture_creation(self):
        """Test creating an architecture"""
        config = {'param1': 10, 'param2': 'value'}
        arch = Architecture(config)
        self.assertEqual(arch.config, config)
        self.assertIsNone(arch.score)
    
    def test_architecture_with_score(self):
        """Test creating an architecture with score"""
        config = {'param1': 10}
        score = 0.85
        arch = Architecture(config, score)
        self.assertEqual(arch.score, score)
    
    def test_architecture_equality(self):
        """Test architecture equality based on config"""
        config1 = {'a': 1, 'b': 2}
        config2 = {'a': 1, 'b': 2}
        config3 = {'a': 2, 'b': 1}
        
        arch1 = Architecture(config1)
        arch2 = Architecture(config2)
        arch3 = Architecture(config3)
        
        self.assertEqual(arch1, arch2)
        self.assertNotEqual(arch1, arch3)


class TestAgents(unittest.TestCase):
    """Test agent classes"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.search_space = {
            'param1': [1, 2, 3],
            'param2': ['a', 'b', 'c']
        }
    
    def test_random_agent_proposal(self):
        """Test RandomSearchAgent proposes valid architectures"""
        agent = RandomSearchAgent(0, self.search_space)
        
        for _ in range(10):
            arch = agent.propose_architecture()
            self.assertIn(arch.config['param1'], self.search_space['param1'])
            self.assertIn(arch.config['param2'], self.search_space['param2'])
    
    def test_random_agent_update(self):
        """Test RandomSearchAgent updates correctly"""
        agent = RandomSearchAgent(0, self.search_space)
        arch = Architecture({'param1': 1, 'param2': 'a'})
        
        agent.update(arch, 0.8)
        
        self.assertEqual(agent.best_architecture, arch)
        self.assertEqual(arch.score, 0.8)
        self.assertEqual(len(agent.history), 1)
    
    def test_greedy_agent_proposal(self):
        """Test GreedySearchAgent proposes valid architectures"""
        agent = GreedySearchAgent(0, self.search_space)
        
        for _ in range(10):
            arch = agent.propose_architecture()
            self.assertIn(arch.config['param1'], self.search_space['param1'])
            self.assertIn(arch.config['param2'], self.search_space['param2'])
    
    def test_greedy_agent_exploitation(self):
        """Test GreedySearchAgent exploits good configurations"""
        agent = GreedySearchAgent(0, self.search_space)
        agent.exploration_rate = 0.0  # No exploration for this test
        
        # Set a best architecture
        best_arch = Architecture({'param1': 2, 'param2': 'b'})
        agent.update(best_arch, 0.9)
        
        # Next proposals should be based on best_arch
        for _ in range(5):
            arch = agent.propose_architecture()
            # At least one parameter should match best configuration
            matches = sum([
                arch.config['param1'] == best_arch.config['param1'],
                arch.config['param2'] == best_arch.config['param2']
            ])
            self.assertGreater(matches, 0)
    
    def test_knowledge_sharing(self):
        """Test agents can share knowledge"""
        agent1 = RandomSearchAgent(0, self.search_space)
        agent2 = RandomSearchAgent(1, self.search_space)
        
        # Agent1 has better architecture
        arch1 = Architecture({'param1': 1, 'param2': 'a'})
        agent1.update(arch1, 0.9)
        
        # Agent2 has worse architecture
        arch2 = Architecture({'param1': 2, 'param2': 'b'})
        agent2.update(arch2, 0.5)
        
        # Share knowledge
        agent1.share_knowledge(agent2)
        
        # Agent2 should now have agent1's best architecture
        self.assertEqual(agent2.best_architecture, arch1)


class TestCoordinator(unittest.TestCase):
    """Test MultiAgentSearchCoordinator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.search_space = {
            'x': [1, 2, 3, 4, 5],
            'y': [10, 20, 30]
        }
        
        def eval_fn(config):
            # Simple evaluation: prefer x=4, y=20
            score = 0.0
            if config['x'] == 4:
                score += 0.5
            if config['y'] == 20:
                score += 0.5
            return score
        
        self.eval_fn = eval_fn
    
    def test_coordinator_initialization(self):
        """Test coordinator initializes correctly"""
        coordinator = MultiAgentSearchCoordinator(
            search_space=self.search_space,
            evaluation_fn=self.eval_fn,
            num_agents=4
        )
        
        self.assertEqual(len(coordinator.agents), 4)
        self.assertEqual(coordinator.num_agents, 4)
        self.assertIsNone(coordinator.best_architecture)
    
    def test_coordinator_search(self):
        """Test coordinator performs search"""
        coordinator = MultiAgentSearchCoordinator(
            search_space=self.search_space,
            evaluation_fn=self.eval_fn,
            num_agents=3,
            agent_types=['random', 'greedy', 'random']
        )
        
        best = coordinator.search(num_iterations=20, verbose=False)
        
        self.assertIsNotNone(best)
        self.assertIsNotNone(best.score)
        self.assertGreater(len(coordinator.evaluated_architectures), 0)
    
    def test_coordinator_finds_optimum(self):
        """Test coordinator can find optimal configuration"""
        coordinator = MultiAgentSearchCoordinator(
            search_space=self.search_space,
            evaluation_fn=self.eval_fn,
            num_agents=4
        )
        
        best = coordinator.search(num_iterations=30, verbose=False)
        
        # Should find or get close to optimal (x=4, y=20, score=1.0)
        self.assertGreater(best.score, 0.5)
    
    def test_coordinator_statistics(self):
        """Test coordinator provides statistics"""
        coordinator = MultiAgentSearchCoordinator(
            search_space=self.search_space,
            evaluation_fn=self.eval_fn,
            num_agents=2
        )
        
        coordinator.search(num_iterations=10, verbose=False)
        stats = coordinator.get_statistics()
        
        self.assertIn('best_score', stats)
        self.assertIn('best_config', stats)
        self.assertIn('num_evaluated', stats)
        self.assertIn('agent_best_scores', stats)
        self.assertEqual(len(stats['agent_best_scores']), 2)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_full_search_workflow(self):
        """Test complete search workflow"""
        # Define search space
        search_space = {
            'learning_rate': [0.001, 0.01, 0.1],
            'batch_size': [16, 32, 64],
            'layers': [2, 3, 4]
        }
        
        # Define evaluation function
        def evaluate(config):
            score = 0.5
            if config['learning_rate'] == 0.01:
                score += 0.2
            if config['batch_size'] == 32:
                score += 0.2
            if config['layers'] >= 3:
                score += 0.1
            return score
        
        # Create and run search
        coordinator = MultiAgentSearchCoordinator(
            search_space=search_space,
            evaluation_fn=evaluate,
            num_agents=3,
            agent_types=['random', 'greedy', 'greedy']
        )
        
        best = coordinator.search(
            num_iterations=25,
            communication_interval=5,
            verbose=False
        )
        
        # Verify results
        self.assertIsNotNone(best)
        self.assertGreater(best.score, 0.5)
        self.assertIn('learning_rate', best.config)
        self.assertIn('batch_size', best.config)
        self.assertIn('layers', best.config)
        
        # Check statistics
        stats = coordinator.get_statistics()
        self.assertGreater(stats['num_evaluated'], 0)
        self.assertLessEqual(stats['num_evaluated'], 25 * 3)  # Max evaluations


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    run_tests()
