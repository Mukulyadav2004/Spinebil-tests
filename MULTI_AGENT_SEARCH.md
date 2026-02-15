# Requirements Document: Insight Agents System

## Introduction

The Insight Agents (IA) system is a conversational, multi-agent platform designed to help e-commerce sellers convert complex business data into actionable insights. Unlike traditional monolithic seller assistants that provide shallow, rule-based responses, IA uses a hierarchical multi-agent architecture with a Manager Agent coordinating specialized Worker Agents to deliver deep diagnostic analysis across multiple business dimensions (sales, pricing, inventory, reviews, traffic).

The system excels at answering vague, diagnostic questions like "How is my business really doing?" by breaking queries into granular steps, reasoning across multiple data sources, and providing both explanations and actionable recommendations.

## Glossary

- **Manager_Agent**: The control layer agent responsible for query routing, augmentation, and safety enforcement
- **Worker_Agent**: Specialized agents that execute specific tasks (Data Presenter or Insight Generator)
- **Data_Presenter_Agent**: Worker agent that retrieves and presents data using API calls and function execution
- **Insight_Generator_Agent**: Worker agent that performs deep analytical reasoning across multiple business dimensions
- **OOD_Detection**: Out-of-domain detection mechanism that identifies queries outside system capabilities
- **Query_Augmenter**: Component that enhances user queries with additional context or structure
- **Data_Workflow_Planner**: Component that decomposes tasks, selects APIs, and formulates inputs
- **Memory_System**: Shared context storage used by all worker agents to maintain conversation state
- **Tool_Library**: Collection of APIs and functions available to worker agents
- **Guardrails**: Safety and policy enforcement mechanisms applied to system outputs
- **Seller**: E-commerce business owner or operator using the system
- **Business_Dimension**: Category of business data (sales, pricing, inventory, reviews, traffic, account metrics)

## Requirements

### Requirement 1: Out-of-Domain Query Detection

**User Story:** As a seller, I want the system to recognize when my question is outside its capabilities, so that I receive honest feedback rather than incorrect or fabricated answers.

#### Acceptance Criteria

1. WHEN a user submits a query, THE Manager_Agent SHALL evaluate whether the query falls within supported business dimensions
2. IF a query is detected as out-of-domain, THEN THE Manager_Agent SHALL reject the query and provide a clear explanation of system capabilities
3. WHEN an out-of-domain query is detected, THE System SHALL NOT route the query to any Worker_Agent
4. THE OOD_Detection SHALL evaluate queries before any routing or processing occurs

### Requirement 2: Intelligent Query Routing

**User Story:** As a seller, I want my questions automatically directed to the right analysis capability, so that I get the most relevant type of response without having to understand system internals.

#### Acceptance Criteria

1. WHEN a user submits an in-domain query, THE Manager_Agent SHALL determine whether the query requires data presentation or insight generation
2. WHEN a query requests factual data or metric summaries, THE Manager_Agent SHALL route to the Data_Presenter_Agent
3. WHEN a query requests diagnostic analysis or causal reasoning, THE Manager_Agent SHALL route to the Insight_Generator_Agent
4. THE Manager_Agent SHALL complete routing decisions before any worker agent execution begins

### Requirement 3: Query Enhancement

**User Story:** As a seller, I want to ask vague questions in natural language, so that I don't need to learn specific query syntax or provide excessive detail.

#### Acceptance Criteria

1. WHEN a user submits a vague or underspecified query, THE Query_Augmenter SHALL enhance the query with additional context
2. THE Query_Augmenter SHALL preserve the original user intent while adding clarifying details
3. WHEN query augmentation is complete, THE Manager_Agent SHALL use the augmented query for routing and execution
4. THE System SHALL maintain both original and augmented query versions in the Memory_System

### Requirement 4: Data Retrieval and Presentation

**User Story:** As a seller, I want to retrieve specific business metrics and data points, so that I can understand what is happening in my business.

#### Acceptance Criteria

1. WHEN the Data_Presenter_Agent receives a routed query, THE Data_Workflow_Planner SHALL decompose the query into discrete data retrieval tasks
2. WHEN tasks are identified, THE Data_Workflow_Planner SHALL select appropriate APIs and functions from the Tool_Library
3. WHEN API selection is complete, THE Executor SHALL retrieve data by calling the selected APIs with formulated inputs
4. WHEN data retrieval is complete, THE Executor SHALL apply post-processing to format results
5. WHEN processing is complete, THE Data_Presenter_Agent SHALL generate a natural language response presenting the data
6. THE Data_Presenter_Agent SHALL store retrieved data in the Memory_System for potential reuse

### Requirement 5: Multi-Dimensional Insight Generation

**User Story:** As a seller, I want to understand why my business is performing a certain way, so that I can make informed decisions about pricing, inventory, and strategy.

#### Acceptance Criteria

1. WHEN the Insight_Generator_Agent receives a routed query, THE Data_Workflow_Executor SHALL decompose the query into analytical tasks spanning multiple business dimensions
2. WHEN analytical tasks are identified, THE Data_Workflow_Executor SHALL perform domain-aware routing to determine which business dimensions to analyze
3. WHEN dimensions are identified, THE Insight_Generator_Agent SHALL retrieve relevant data across sales, pricing, inventory, reviews, and traffic dimensions
4. WHEN data is retrieved, THE Insight_Generator_Agent SHALL apply analytical reasoning to identify causal relationships and patterns
5. WHEN analysis is complete, THE Insight_Generator_Agent SHALL generate insights using customized prompting techniques
6. THE Insight_Generator_Agent SHALL provide both explanatory insights (why something happened) and actionable recommendations (what to do next)

### Requirement 6: Shared Memory Management

**User Story:** As a seller, I want the system to remember context from earlier in our conversation, so that I can ask follow-up questions without repeating information.

#### Acceptance Criteria

1. WHEN any Worker_Agent retrieves data or generates insights, THE System SHALL store relevant context in the Memory_System
2. WHEN a Worker_Agent begins processing a query, THE System SHALL provide access to relevant historical context from the Memory_System
3. THE Memory_System SHALL maintain conversation state across multiple query-response cycles
4. WHEN context is stored, THE Memory_System SHALL associate it with the current conversation session

### Requirement 7: Tool and API Integration

**User Story:** As a system administrator, I want worker agents to access business data through a unified tool library, so that data retrieval is consistent and maintainable.

#### Acceptance Criteria

1. THE Tool_Library SHALL provide a unified interface for all available APIs and functions
2. WHEN a Worker_Agent requests data, THE Tool_Library SHALL execute the appropriate API call with provided parameters
3. WHEN API calls complete, THE Tool_Library SHALL return structured results to the requesting Worker_Agent
4. THE Tool_Library SHALL handle API errors and return meaningful error messages to Worker_Agents

### Requirement 8: Response Safety and Policy Enforcement

**User Story:** As a platform operator, I want all system responses to comply with safety policies and business rules, so that sellers receive appropriate and compliant information.

#### Acceptance Criteria

1. WHEN a Worker_Agent generates a response, THE Manager_Agent SHALL apply guardrails before returning results to the user
2. THE Guardrails SHALL evaluate responses for policy violations, inappropriate content, or unsafe recommendations
3. IF a response violates policies, THEN THE Manager_Agent SHALL modify or reject the response
4. WHEN guardrails are satisfied, THE Manager_Agent SHALL return the approved response to the user

### Requirement 9: Advanced Diagnostic Reasoning

**User Story:** As a seller, I want to ask complex diagnostic questions that require reasoning across multiple business areas, so that I can understand interconnected issues affecting my business.

#### Acceptance Criteria

1. WHEN a diagnostic query involves multiple business dimensions, THE Insight_Generator_Agent SHALL analyze relationships between dimensions
2. WHEN analyzing relationships, THE Insight_Generator_Agent SHALL identify correlations, causal factors, and compounding effects
3. WHEN multiple factors contribute to a business outcome, THE Insight_Generator_Agent SHALL explain the relative impact of each factor
4. THE Insight_Generator_Agent SHALL provide specific, quantified recommendations when sufficient data is available

### Requirement 10: Task Decomposition and Planning

**User Story:** As a seller, I want complex questions broken down into manageable analytical steps, so that the system provides complete and thorough answers.

#### Acceptance Criteria

1. WHEN a Worker_Agent receives a complex query, THE Data_Workflow_Planner or Data_Workflow_Executor SHALL decompose it into granular sub-tasks
2. THE System SHALL ensure all necessary sub-tasks are identified before execution begins
3. WHEN sub-tasks are executed, THE System SHALL track completion status to ensure no steps are skipped
4. WHEN all sub-tasks complete, THE Worker_Agent SHALL aggregate results into a coherent response

### Requirement 11: Customized Prompting for Insights

**User Story:** As a system designer, I want the Insight Generator to use specialized prompting techniques, so that analytical responses are higher quality than generic LLM outputs.

#### Acceptance Criteria

1. WHEN generating insights, THE Insight_Generator_Agent SHALL use customized prompting that includes chain-of-thought reasoning
2. WHERE few-shot examples are available, THE Insight_Generator_Agent SHALL inject relevant examples into prompts
3. THE Insight_Generator_Agent SHALL use domain-specific prompting strategies different from the Data_Presenter_Agent
4. WHEN prompting techniques are applied, THE System SHALL generate responses that demonstrate explicit reasoning steps

### Requirement 12: Results Aggregation

**User Story:** As a seller, I want responses from multiple analytical steps combined into a single coherent answer, so that I don't receive fragmented or confusing information.

#### Acceptance Criteria

1. WHEN a Worker_Agent completes multiple sub-tasks, THE System SHALL aggregate results before generating the final response
2. THE System SHALL resolve any conflicts or inconsistencies between sub-task results
3. WHEN aggregation is complete, THE System SHALL present a unified response that addresses the original query
4. THE System SHALL maintain logical flow and coherence across aggregated results
