#!/usr/bin/env python3
"""
Creating Swarm of Agents using Strands Agents

This module provides comprehensive examples and implementations of multi-agent swarm systems
using the Strands Agents SDK. It demonstrates both built-in swarm tools and custom mesh
architecture implementations for collaborative problem solving.

The module covers:
- Swarm intelligence principles and multi-agent system concepts
- Built-in swarm tool usage with coordination patterns
- Custom mesh architecture implementation
- Shared memory systems for agent collaboration
- Practical examples and demonstrations
"""

import time
import threading
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Third-party imports
try:
    from strands import Agent
    from strands_tools import swarm
    STRANDS_AVAILABLE = True
except ImportError:
    print("Warning: Strands SDK not available. Some functions will be limited to demonstration mode.")
    STRANDS_AVAILABLE = False


# ==============================================================================
# MULTI-AGENT SYSTEMS AND SWARM INTELLIGENCE CONCEPTS
# ==============================================================================

class SwarmIntelligenceConcepts:
    """
    Educational class explaining multi-agent systems and swarm intelligence principles.
    
    This class provides comprehensive documentation of the theoretical foundations
    that underpin effective swarm agent implementations.
    """
    
    @staticmethod
    def what_is_agent_swarm() -> str:
        """
        Explains the fundamental concept of agent swarms.
        
        Returns:
            Detailed explanation of agent swarm concepts
        """
        return """
        AGENT SWARM DEFINITION:
        An agent swarm is a collection of autonomous AI agents working together to solve 
        complex problems through collaboration. Inspired by natural systems like ant colonies 
        or bird flocks, agent swarms leverage collective intelligence where the combined output 
        exceeds what any single agent could produce.
        
        KEY CHARACTERISTICS:
        • Autonomous agents with specialized capabilities
        • Collaborative problem-solving through information sharing
        • Emergent intelligence from collective behavior
        • Distributed processing for improved efficiency
        • Fault tolerance through redundancy and cooperation
        
        ADVANTAGES OVER SINGLE AGENTS:
        • Can tackle complex, multi-faceted problems
        • Parallel processing reduces overall completion time
        • Multiple perspectives improve solution quality
        • Natural fault tolerance and error correction
        • Scalable architecture for varying problem complexity
        """
    
    @staticmethod
    def multi_agent_system_capabilities() -> Dict[str, str]:
        """
        Describes the core capabilities enabled by multi-agent systems.
        
        Returns:
            Dictionary mapping capability names to descriptions
        """
        return {
            "distributed_problem_solving": """
                Breaking complex tasks into subtasks for parallel processing.
                Each agent can work on different aspects simultaneously, dramatically
                reducing the time required for comprehensive analysis.
            """,
            
            "information_sharing": """
                Agents exchange insights to build collective knowledge.
                Through shared memory or direct communication, agents can leverage
                discoveries made by other agents to enhance their own analysis.
            """,
            
            "specialization": """
                Different agents focus on specific aspects of a problem.
                Specialized agents develop deep expertise in their domain,
                leading to higher quality analysis than generalist approaches.
            """,
            
            "redundancy": """
                Multiple agents working on similar tasks improve reliability.
                Cross-validation and consensus-building reduce errors and
                increase confidence in the final results.
            """,
            
            "emergent_intelligence": """
                The system exhibits capabilities beyond individual components.
                Complex behaviors and insights emerge from the interaction of
                simple agent rules and communication patterns.
            """
        }
    
    @staticmethod
    def swarm_intelligence_principles() -> Dict[str, str]:
        """
        Outlines the key principles of swarm intelligence.
        
        Returns:
            Dictionary mapping principle names to descriptions
        """
        return {
            "decentralized_control": """
                No single agent directs the entire system.
                Control emerges from the collective behavior of all agents,
                making the system more robust and adaptable.
            """,
            
            "local_interactions": """
                Agents primarily interact with nearby agents.
                Local communication patterns create efficient information flow
                while avoiding the complexity of global coordination.
            """,
            
            "simple_rules": """
                Individual agents follow relatively simple behaviors.
                Complexity emerges from the interaction of simple rules rather
                than from complex individual agent programming.
            """,
            
            "emergent_complexity": """
                Complex system behavior emerges from simple agent interactions.
                The swarm exhibits sophisticated problem-solving capabilities
                that exceed the sum of individual agent capabilities.
            """
        }


# ==============================================================================
# SHARED MEMORY SYSTEM FOR AGENT COLLABORATION
# ==============================================================================

@dataclass
class AgentContribution:
    """
    Represents a single contribution from an agent to shared memory.
    
    Attributes:
        agent_id: Identifier of the contributing agent
        content: The actual contribution content
        phase: Processing phase when contribution was made
        timestamp: When the contribution was created
        metadata: Additional information about the contribution
    """
    agent_id: str
    content: str
    phase: int
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


class SharedMemory:
    """
    Thread-safe shared memory system for agent collaboration.
    
    This class implements a centralized knowledge repository that enables
    multiple agents to share information, track processing phases, and
    maintain historical knowledge across swarm operations.
    """
    
    def __init__(self):
        """Initialize the shared memory system with thread safety."""
        self._contributions: List[AgentContribution] = []
        self._current_phase = 0
        self._lock = threading.RLock()
        self._phase_history: Dict[int, List[AgentContribution]] = {}
    
    def add_contribution(self, agent_id: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a contribution from an agent to shared memory.
        
        Args:
            agent_id: Identifier of the contributing agent
            content: The contribution content
            metadata: Optional additional information
        """
        with self._lock:
            contribution = AgentContribution(
                agent_id=agent_id,
                content=content,
                phase=self._current_phase,
                timestamp=datetime.now(),
                metadata=metadata or {}
            )
            
            self._contributions.append(contribution)
            
            # Track contributions by phase
            if self._current_phase not in self._phase_history:
                self._phase_history[self._current_phase] = []
            self._phase_history[self._current_phase].append(contribution)
    
    def get_contributions(self, 
                         phase: Optional[int] = None,
                         agent_id: Optional[str] = None,
                         include_history: bool = False) -> List[AgentContribution]:
        """
        Retrieve contributions from shared memory.
        
        Args:
            phase: Specific phase to retrieve (None for current phase)
            agent_id: Specific agent contributions (None for all agents)
            include_history: Whether to include historical phases
            
        Returns:
            List of matching contributions
        """
        with self._lock:
            if phase is None:
                phase = self._current_phase
            
            if include_history:
                # Get all contributions up to specified phase
                contributions = []
                for p in range(phase + 1):
                    contributions.extend(self._phase_history.get(p, []))
            else:
                # Get contributions for specific phase only
                contributions = self._phase_history.get(phase, [])
            
            if agent_id is not None:
                contributions = [c for c in contributions if c.agent_id == agent_id]
            
            return contributions
    
    def advance_phase(self) -> int:
        """
        Advance to the next processing phase.
        
        Returns:
            The new current phase number
        """
        with self._lock:
            self._current_phase += 1
            return self._current_phase
    
    def get_current_phase(self) -> int:
        """
        Get the current processing phase.
        
        Returns:
            Current phase number
        """
        with self._lock:
            return self._current_phase
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of shared memory contents.
        
        Returns:
            Dictionary with memory statistics and contents
        """
        with self._lock:
            return {
                "total_contributions": len(self._contributions),
                "current_phase": self._current_phase,
                "phases": list(self._phase_history.keys()),
                "agents": list(set(c.agent_id for c in self._contributions)),
                "contributions_by_phase": {
                    phase: len(contributions) 
                    for phase, contributions in self._phase_history.items()
                }
            }
    
    def clear(self) -> None:
        """Clear all contributions and reset to phase 0."""
        with self._lock:
            self._contributions.clear()
            self._phase_history.clear()
            self._current_phase = 0


# ==============================================================================
# BUILT-IN SWARM TOOL DEMONSTRATIONS
# ==============================================================================

class BuiltInSwarmExamples:
    """
    Demonstrations of the built-in swarm tool from Strands Agents SDK.
    
    This class provides practical examples of using the swarm tool for
    various coordination patterns and problem-solving scenarios.
    """
    
    def __init__(self):
        """Initialize the swarm examples with an agent if Strands is available."""
        if STRANDS_AVAILABLE:
            self.agent = Agent(tools=[swarm])
        else:
            self.agent = None
            print("Strands SDK not available - running in demonstration mode")
    
    def demonstrate_direct_tool_invocation(self, task: str = "Analyze this scientific paper and identify key findings") -> Dict[str, Any]:
        """
        Demonstrate direct invocation of the swarm tool.
        
        Args:
            task: The task to be processed by the swarm
            
        Returns:
            Swarm analysis results or demo output
        """
        if not STRANDS_AVAILABLE:
            return {
                "demo_mode": True,
                "message": "Would invoke swarm tool with collaborative pattern",
                "task": task,
                "swarm_size": 5
            }
        
        print("🔄 Running collaborative swarm analysis...")
        result = self.agent.tool.swarm(
            task=task,
            swarm_size=5,
            coordination_pattern="collaborative",
        )
        
        print("✅ Collaborative analysis complete")
        return result
    
    def demonstrate_competitive_pattern(self, task: str = "Analyze this scientific paper and identify key findings") -> Dict[str, Any]:
        """
        Demonstrate competitive coordination pattern.
        
        Args:
            task: The task to be processed by the swarm
            
        Returns:
            Swarm analysis results or demo output
        """
        if not STRANDS_AVAILABLE:
            return {
                "demo_mode": True,
                "message": "Would invoke swarm tool with competitive pattern",
                "task": task,
                "swarm_size": 5
            }
        
        print("🔄 Running competitive swarm analysis...")
        result = self.agent.tool.swarm(
            task=task,
            swarm_size=5,
            coordination_pattern="competitive",
        )
        
        print("✅ Competitive analysis complete")
        return result
    
    def demonstrate_natural_language_invocation(self, query: str = "Use a swarm of 4 agents to analyze the current market trend for generative ai based agents.") -> str:
        """
        Demonstrate natural language invocation of swarm capabilities.
        
        Args:
            query: Natural language query that will trigger swarm usage
            
        Returns:
            Agent response or demo output
        """
        if not STRANDS_AVAILABLE:
            return f"Demo mode: Would process query '{query}' using natural language swarm invocation"
        
        print("🔄 Processing natural language swarm query...")
        result = str(self.agent(query))
        print("✅ Natural language swarm analysis complete")
        
        return result
    
    def explain_coordination_patterns(self) -> Dict[str, str]:
        """
        Explain the different coordination patterns available in the swarm tool.
        
        Returns:
            Dictionary mapping pattern names to descriptions
        """
        return {
            "collaborative": """
                Agents build upon others' insights and seek consensus.
                - Agents share information freely
                - Build upon previous contributions
                - Work toward common understanding
                - Emphasizes agreement and synthesis
            """,
            
            "competitive": """
                Agents develop independent solutions and unique perspectives.
                - Agents work independently first
                - Present diverse viewpoints
                - Challenge each other's ideas  
                - Emphasizes diversity and debate
            """,
            
            "hybrid": """
                Balances cooperation with independent exploration.
                - Combines collaborative and competitive elements
                - Allows for both consensus building and diverse perspectives
                - Adapts strategy based on problem requirements
                - Provides balanced approach to complex problems
            """
        }


# ==============================================================================
# CUSTOM MESH SWARM ARCHITECTURE
# ==============================================================================

class MeshSwarmAgent:
    """
    Represents an individual agent in a mesh swarm architecture.
    
    This class wraps a Strands Agent with mesh communication capabilities,
    allowing direct communication with all other agents in the swarm.
    """
    
    def __init__(self, agent_id: str, system_prompt: str, shared_memory: SharedMemory):
        """
        Initialize a mesh swarm agent.
        
        Args:
            agent_id: Unique identifier for this agent
            system_prompt: System prompt defining the agent's role
            shared_memory: Shared memory system for communication
        """
        self.agent_id = agent_id
        self.shared_memory = shared_memory
        
        if STRANDS_AVAILABLE:
            self.agent = Agent(system_prompt=system_prompt, callback_handler=None)
        else:
            self.agent = None
            print(f"Demo mode: Created agent {agent_id} with role defined by system prompt")
    
    def process(self, query: str, include_peer_inputs: bool = True) -> str:
        """
        Process a query, optionally incorporating peer agent inputs.
        
        Args:
            query: The query to process
            include_peer_inputs: Whether to include inputs from other agents
            
        Returns:
            Agent's response to the query
        """
        if not STRANDS_AVAILABLE:
            return f"Demo mode: Agent {self.agent_id} would process query '{query[:50]}...'"
        
        # Construct prompt with peer inputs if requested
        if include_peer_inputs:
            peer_contributions = self.shared_memory.get_contributions()
            peer_inputs = []
            
            for contribution in peer_contributions:
                if contribution.agent_id != self.agent_id:  # Exclude own contributions
                    peer_inputs.append(f"From {contribution.agent_id}: {contribution.content}")
            
            if peer_inputs:
                enhanced_query = f"{query}\n\nConsider these insights from other agents:\n" + "\n\n".join(peer_inputs)
            else:
                enhanced_query = query
        else:
            enhanced_query = query
        
        # Process the query
        result = str(self.agent(enhanced_query))
        
        # Add result to shared memory
        self.shared_memory.add_contribution(
            agent_id=self.agent_id,
            content=result,
            metadata={"query": query, "include_peer_inputs": include_peer_inputs}
        )
        
        return result


class MeshSwarm:
    """
    Implementation of a mesh architecture swarm where all agents can communicate directly.
    
    In a mesh architecture, every agent can communicate with every other agent,
    enabling flexible information sharing and collaborative problem solving.
    """
    
    def __init__(self):
        """Initialize the mesh swarm with shared memory."""
        self.shared_memory = SharedMemory()
        self.agents: Dict[str, MeshSwarmAgent] = {}
    
    def add_agent(self, agent_id: str, system_prompt: str) -> MeshSwarmAgent:
        """
        Add an agent to the mesh swarm.
        
        Args:
            agent_id: Unique identifier for the agent
            system_prompt: System prompt defining the agent's role
            
        Returns:
            The created MeshSwarmAgent
        """
        agent = MeshSwarmAgent(agent_id, system_prompt, self.shared_memory)
        self.agents[agent_id] = agent
        return agent
    
    def process_query_mesh(self, query: str, phases: int = 2, delay_between_agents: int = 5) -> Dict[str, Any]:
        """
        Process a query using mesh communication across multiple phases.
        
        Args:
            query: The query to process
            phases: Number of processing phases
            delay_between_agents: Delay in seconds between agent calls
            
        Returns:
            Dictionary with results from all phases and agents
        """
        results = {
            "query": query,
            "phases": phases,
            "phase_results": {},
            "final_synthesis": None
        }
        
        print(f"🔄 Processing query across {phases} phases with {len(self.agents)} agents")
        
        for phase in range(phases):
            print(f"📍 Phase {phase + 1}")
            phase_results = {}
            
            # In mesh architecture, all agents process in parallel but we'll simulate sequentially
            for agent_id, agent in self.agents.items():
                if agent_id == "summarizer" and phase == 0:
                    # Summarizer waits for other agents in first phase
                    continue
                
                print(f"  🤖 {agent_id} processing...")
                
                # Include peer inputs from current phase onward
                include_peers = phase > 0 or agent_id == "summarizer"
                result = agent.process(query, include_peer_inputs=include_peers)
                phase_results[agent_id] = result
                
                if delay_between_agents > 0:
                    time.sleep(delay_between_agents)
            
            results["phase_results"][f"phase_{phase + 1}"] = phase_results
            
            # Advance to next phase
            if phase < phases - 1:
                self.shared_memory.advance_phase()
        
        # Get final synthesis from summarizer if available
        if "summarizer" in self.agents:
            print("📝 Creating final synthesis...")
            synthesis_result = self.agents["summarizer"].process(
                f"Create a comprehensive final synthesis for: {query}",
                include_peer_inputs=True
            )
            results["final_synthesis"] = synthesis_result
        
        print("✅ Mesh swarm processing complete")
        return results
    
    def get_swarm_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the swarm's current state and memory contents.
        
        Returns:
            Dictionary with swarm statistics and memory summary
        """
        return {
            "agent_count": len(self.agents),
            "agent_ids": list(self.agents.keys()),
            "memory_summary": self.shared_memory.get_summary()
        }


# ==============================================================================
# DEMONSTRATION AND EXAMPLE FUNCTIONS
# ==============================================================================

def create_specialized_mesh_swarm() -> MeshSwarm:
    """
    Create a mesh swarm with specialized agents for comprehensive analysis.
    
    Returns:
        Configured MeshSwarm with specialized agents
    """
    swarm = MeshSwarm()
    
    # Research specialist
    swarm.add_agent("research", """You are a Research Agent specializing in gathering and analyzing information.
Your role in the swarm is to provide factual information and research insights on the topic.
You should focus on providing accurate data and identifying key aspects of the problem.
When receiving input from other agents, evaluate if their information aligns with your research.""")
    
    # Creative specialist
    swarm.add_agent("creative", """You are a Creative Agent specializing in generating innovative solutions.
Your role in the swarm is to think outside the box and propose creative approaches.
You should build upon information from other agents while adding your unique creative perspective.
Focus on novel approaches that others might not have considered.""")
    
    # Critical analyst
    swarm.add_agent("critical", """You are a Critical Agent specializing in analyzing proposals and finding flaws.
Your role in the swarm is to evaluate solutions proposed by other agents and identify potential issues.
You should carefully examine proposed solutions, find weaknesses or oversights, and suggest improvements.
Be constructive in your criticism while ensuring the final solution is robust.""")
    
    # Synthesizer
    swarm.add_agent("summarizer", """You are a Summarizer Agent specializing in synthesizing information.
Your role in the swarm is to gather insights from all agents and create a cohesive final solution.
You should combine the best ideas and address the criticisms to create a comprehensive response.
Focus on creating a clear, actionable summary that addresses the original query effectively.""")
    
    return swarm


def demonstrate_swarm_concepts():
    """
    Comprehensive demonstration of swarm concepts and implementations.
    
    This function provides an interactive tour of swarm intelligence principles,
    built-in tools, and custom mesh architecture implementations.
    """
    print("🐝 SWARM INTELLIGENCE DEMONSTRATION")
    print("=" * 60)
    
    # 1. Explain core concepts
    print("\n📚 SWARM INTELLIGENCE CONCEPTS")
    concepts = SwarmIntelligenceConcepts()
    print(concepts.what_is_agent_swarm())
    
    # 2. Show multi-agent capabilities
    print("\n🤝 MULTI-AGENT SYSTEM CAPABILITIES")
    capabilities = concepts.multi_agent_system_capabilities()
    for name, description in capabilities.items():
        print(f"• {name.replace('_', ' ').title()}: {description.strip()}")
    
    # 3. Demonstrate built-in swarm tool
    print("\n🛠️  BUILT-IN SWARM TOOL DEMONSTRATION")
    swarm_examples = BuiltInSwarmExamples()
    
    # Show coordination patterns
    patterns = swarm_examples.explain_coordination_patterns()
    print("Available coordination patterns:")
    for pattern, description in patterns.items():
        print(f"• {pattern.title()}: {description.strip()}")
    
    # 4. Create and demonstrate mesh swarm
    print("\n🕸️  MESH SWARM ARCHITECTURE DEMONSTRATION")
    mesh_swarm = create_specialized_mesh_swarm()
    
    print(f"Created mesh swarm with {len(mesh_swarm.agents)} specialized agents:")
    for agent_id in mesh_swarm.agents.keys():
        print(f"  • {agent_id}")
    
    # 5. Show shared memory system
    print("\n🧠 SHARED MEMORY SYSTEM")
    memory_summary = mesh_swarm.get_swarm_summary()
    print(f"Memory system initialized with {memory_summary['agent_count']} agents")
    print(f"Current phase: {memory_summary['memory_summary']['current_phase']}")
    
    print("\n✅ Swarm demonstration complete!")
    return mesh_swarm


def run_mesh_swarm_example(query: str = "Generative AI trends and implications") -> Dict[str, Any]:
    """
    Run a complete mesh swarm analysis example.
    
    Args:
        query: The query to analyze with the mesh swarm
        
    Returns:
        Complete results from the mesh swarm analysis
    """
    print(f"🚀 Running mesh swarm analysis on: '{query}'")
    
    # Create the specialized mesh swarm
    mesh_swarm = create_specialized_mesh_swarm()
    
    # Process the query through the mesh
    results = mesh_swarm.process_query_mesh(
        query=query,
        phases=2,
        delay_between_agents=2  # Reduced delay for demo
    )
    
    return results


def when_to_use_swarms() -> Dict[str, List[str]]:
    """
    Guidance on when to use swarm architectures vs single agents.
    
    Returns:
        Dictionary with use case categories and examples
    """
    return {
        "ideal_for_swarms": [
            "Complex, multi-faceted problems requiring diverse expertise",
            "Tasks that benefit from multiple perspectives and validation",
            "Problems where parallel processing provides significant speedup",
            "Analysis requiring consensus or comprehensive coverage",
            "Creative tasks needing both innovation and critical evaluation",
            "Research problems with multiple data sources and analysis angles"
        ],
        
        "single_agent_preferred": [
            "Simple, well-defined tasks with clear single solutions",
            "Routine operations that don't require multiple perspectives",
            "Tasks where coordination overhead exceeds benefits",
            "Problems with strict sequential dependencies",
            "Resource-constrained environments where efficiency is critical"
        ],
        
        "hybrid_approaches": [
            "Initial swarm analysis followed by single-agent refinement",
            "Single-agent preprocessing with swarm collaboration for complex analysis",
            "Swarm consensus for key decisions with single-agent execution",
            "Hierarchical systems with single-agent coordinators managing swarms"
        ]
    }


# ==============================================================================
# MAIN EXECUTION AND INTERACTIVE EXAMPLES
# ==============================================================================

def main():
    """
    Main function providing interactive swarm demonstrations and examples.
    
    This function serves as the entry point for exploring swarm intelligence
    concepts and implementations when the module is executed directly.
    """
    print(__doc__)
    print("\n🚀 Starting Swarm Intelligence Exploration...")
    
    # Run the comprehensive demonstration
    mesh_swarm = demonstrate_swarm_concepts()
    
    # Provide usage guidance
    print("\n" + "=" * 60)
    print("📋 WHEN TO USE SWARMS")
    usage_guide = when_to_use_swarms()
    
    for category, examples in usage_guide.items():
        print(f"\n{category.replace('_', ' ').title()}:")
        for example in examples:
            print(f"  • {example}")
    
    # Interactive options
    print("\n" + "=" * 60)
    print("🛠️  AVAILABLE FUNCTIONS FOR EXPLORATION:")
    print("  • demonstrate_swarm_concepts() - Full concept demonstration")
    print("  • create_specialized_mesh_swarm() - Create a mesh swarm")
    print("  • run_mesh_swarm_example(query) - Run complete analysis")
    print("  • BuiltInSwarmExamples() - Explore built-in swarm tools")
    print("  • SharedMemory() - Create shared memory system")
    
    print("\n💡 Tip: Import this module to access all swarm classes and functions")
    print("Example: from swarm import MeshSwarm, SharedMemory, demonstrate_swarm_concepts")
    
    return mesh_swarm


if __name__ == "__main__":
    main()