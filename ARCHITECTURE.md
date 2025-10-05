# Multi-Agent Architecture Search - System Architecture

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                  MultiAgentSearchCoordinator                     │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Agent 1   │  │   Agent 2   │  │   Agent 3   │   ...       │
│  │  (Random)   │  │  (Greedy)   │  │  (Random)   │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         │                 │                 │                     │
│         │    Knowledge    │    Sharing      │                     │
│         └────────┬────────┴────────┬────────┘                     │
│                  │                 │                               │
│         ┌────────▼─────────────────▼────────┐                     │
│         │   Best Architecture Tracker       │                     │
│         └───────────────────────────────────┘                     │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              Evaluation Function                            │ │
│  │  (Provided by user - evaluates configurations)             │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Component Hierarchy

```
Architecture
├── config: Dict[str, Any]     # The configuration parameters
└── score: float                # Performance score

Agent (Abstract)
├── agent_id: int
├── search_space: Dict
├── best_architecture: Architecture
├── history: List[Architecture]
├── propose_architecture() → Architecture
├── update(architecture, score)
└── share_knowledge(other_agent)

RandomSearchAgent (extends Agent)
├── propose_architecture() → Architecture
│   └── Returns random configuration from search space
└── update(architecture, score)
    └── Updates best if better score found

GreedySearchAgent (extends Agent)
├── exploration_rate: float (0.3)
├── propose_architecture() → Architecture
│   ├── 30% time: random exploration
│   └── 70% time: mutate best configuration
└── update(architecture, score)
    └── Updates best if better score found

MultiAgentSearchCoordinator
├── agents: List[Agent]
├── search_space: Dict
├── evaluation_fn: Callable
├── best_architecture: Architecture
├── evaluated_architectures: Set
├── search(num_iterations, communication_interval) → Architecture
│   ├── For each iteration:
│   │   ├── Each agent proposes architecture
│   │   ├── Evaluate architecture
│   │   ├── Update agent
│   │   └── Update global best
│   └── Periodically: facilitate_communication()
├── _facilitate_communication()
│   └── Agents share best findings
└── get_statistics() → Dict
    └── Returns search statistics
```

## Search Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         START SEARCH                             │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                    Initialize Agents
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                    ITERATION LOOP                                 │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ For each agent:                                            │  │
│  │                                                            │  │
│  │  1. Agent proposes architecture                           │  │
│  │       │                                                    │  │
│  │       ├─ RandomAgent: Pick random config                  │  │
│  │       └─ GreedyAgent: Mutate best or random               │  │
│  │                                                            │  │
│  │  2. Check if already evaluated                            │  │
│  │       │                                                    │  │
│  │       ├─ Yes: Skip                                         │  │
│  │       └─ No: Continue                                      │  │
│  │                                                            │  │
│  │  3. Evaluate architecture                                 │  │
│  │       └─ Call user's evaluation function                  │  │
│  │                                                            │  │
│  │  4. Update agent with result                              │  │
│  │       └─ Agent updates internal best if better            │  │
│  │                                                            │  │
│  │  5. Update global best                                    │  │
│  │       └─ Coordinator tracks overall best                  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Every N iterations (communication_interval):               │  │
│  │                                                            │  │
│  │   Agents Share Knowledge                                  │  │
│  │       │                                                    │  │
│  │       └─ Each agent shares with random subset of others   │  │
│  │          If agent A's best > agent B's best:              │  │
│  │             B adopts A's best                              │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                    Repeat for N iterations
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RETURN BEST ARCHITECTURE                       │
└─────────────────────────────────────────────────────────────────┘
```

## Agent Communication Pattern

```
Time: t=0
┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
│Agent 1 │  │Agent 2 │  │Agent 3 │  │Agent 4 │
│Best:0.5│  │Best:0.3│  │Best:0.7│  │Best:0.4│
└────────┘  └────────┘  └────────┘  └────────┘

Time: t=10 (Communication interval)
         Knowledge Sharing
┌────────────────────────────────────────┐
│  Agent 1 ←→ Agent 3                    │
│  Agent 1 ←→ Agent 4                    │
│  Agent 2 ←→ Agent 3                    │
│  Agent 2 ←→ Agent 4                    │
└────────────────────────────────────────┘

Time: t=10+ (After sharing)
┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
│Agent 1 │  │Agent 2 │  │Agent 3 │  │Agent 4 │
│Best:0.7│  │Best:0.7│  │Best:0.7│  │Best:0.7│
└────────┘  └────────┘  └────────┘  └────────┘
   All agents now know about Agent 3's discovery!
```

## Search Space Exploration

```
Search Space Visualization:
┌─────────────────────────────────────────┐
│  Random Agent Exploration:              │
│     *      *                *           │
│              *    *                     │
│        *              *        *        │
│                                         │
│  Greedy Agent Exploration:              │
│                 ╔═══╗                   │
│                 ║★★★║  ← Found good     │
│                 ║★★★║     region        │
│                 ╚═══╝                   │
│                                         │
│  Combined Strategy:                     │
│     *      *    ╔═══╗     *            │
│              *  ║★★★║                   │
│        *        ║★★★║  *        *       │
│                 ╚═══╝                   │
└─────────────────────────────────────────┘
Legend:
  * = Random exploration
  ★ = Greedy exploitation
  ╔═╗ = High-quality region
```

## Performance Characteristics

### Time Complexity
- Per iteration: O(num_agents × evaluation_time)
- Total: O(num_iterations × num_agents × evaluation_time)

### Space Complexity
- O(num_evaluated_architectures + num_agents × history_size)

### Scalability
```
Search Space Size  |  Recommended Agents  |  Recommended Iterations
─────────────────────────────────────────────────────────────────
< 100              |  2-3                 |  20-50
100-1,000          |  4-6                 |  50-100
1,000-10,000       |  6-8                 |  100-200
> 10,000           |  8-12                |  200-500
```

## Integration Points

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Application                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Define:                                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 1. search_space = {...}                             │   │
│  │ 2. def evaluate(config): ...                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
└──────────────────────────┼───────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│           MultiAgentSearchCoordinator                        │
│                                                              │
│  coordinator = MultiAgentSearchCoordinator(                 │
│      search_space=search_space,                             │
│      evaluation_fn=evaluate,                                │
│      num_agents=4                                           │
│  )                                                          │
│                                                              │
│  best = coordinator.search(num_iterations=100)              │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Your Application                          │
│                                                              │
│  Use results:                                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ best_config = best.config                           │   │
│  │ best_score = best.score                             │   │
│  │ deploy_configuration(best_config)                   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Extension Points

The framework is designed to be extensible:

1. **Custom Agents**: Subclass `Agent` to implement new search strategies
2. **Custom Communication**: Override `_facilitate_communication()` 
3. **Custom Evaluation**: Any function that takes config → score
4. **Custom Metrics**: Extend `get_statistics()` for more insights

## See Also

- `QUICKSTART.md` - Quick start guide
- `MULTI_AGENT_SEARCH.md` - Detailed documentation
- `examples.py` - Usage examples
- `test_multi_agent_search.py` - Unit tests
