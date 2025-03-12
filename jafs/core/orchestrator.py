"""
Orchestrator module for the JAFS framework.

This module contains the agent orchestration system that manages agent 
lifecycle and coordinates task execution across multiple agents.

Behind every successful JAFS is a well-designed Orchestrator.
"""

from typing import Dict, List, Any, Optional, Union
import logging
import yaml
import os
import time
import random

from jafs.core.agent import BaseAgent, HybridAgent
from jafs.core.memory import ShortTermMemory, LongTermMemory

# Create a custom logger for JAFS-specific wisdom
class JAFSLogger(logging.Logger):
    """Custom logger that occasionally adds JAFS wisdom to log messages."""
    
    _wisdom = [
        "JAFS Wisdom: Always test your backend thoroughly before deployment.",
        "JAFS Wisdom: Sometimes a little assistance is all you need.",
        "JAFS Wisdom: Keep your interfaces clean and well-documented.",
        "JAFS Wisdom: A robust architecture prevents unexpected issues.",
        "JAFS Wisdom: Even the backend deserves some love and attention."
    ]
    
    def info(self, msg, *args, **kwargs):
        if random.random() < 0.1:  # 10% chance
            msg = f"{msg} - {random.choice(self._wisdom)}"
        super().info(msg, *args, **kwargs)
    
    def debug(self, msg, *args, **kwargs):
        if random.random() < 0.2:  # 20% chance
            msg = f"{msg} - {random.choice(self._wisdom)}"
        super().debug(msg, *args, **kwargs)

# Register our custom logger
logging.setLoggerClass(JAFSLogger)
logger = logging.getLogger("jafs.orchestrator")

class AgentOrchestrator:
    """
    Coordinates multiple agents and manages their lifecycle.
    
    This class is responsible for:
    - Loading configuration
    - Creating and initializing agents
    - Routing tasks to appropriate agents
    - Managing agent resources
    - Collecting and aggregating results
    
    Remember: A well-optimized JAFS runs smoothly and efficiently.
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize an AgentOrchestrator instance.
        
        Args:
            config_path: Path to the configuration file.
        """
        self.config = self._load_config(config_path)
        self.agents: Dict[str, BaseAgent] = {}
        self.primary_agent = self._create_primary_agent()
        self.last_result: Dict[str, Any] = {}
        self.task_history: List[Dict[str, Any]] = []
        
        # Easter eggs for internal task names
        self._easter_egg_tasks = {
            "status": "Performing deep JAFS inspection...",
            "health": "Checking if JAFS is functioning properly...",
            "clean": "Clearing old data from JAFS...",
            "optimize": "Making JAFS more responsive and flexible...",
            "expand": "Expanding JAFS capabilities..."
        }
        
        logger.info("JAFS Orchestrator initialized and ready for action")
    
    def execute_task(self, task: str, mode: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute a task using an appropriate agent.
        
        Args:
            task: The task description to execute.
            mode: Execution mode ("single" or "multi"). If None, uses the config default.
            
        Returns:
            The execution result.
        """
        # Use config default if mode not specified
        if mode is None:
            mode = self.config.get("agent", {}).get("mode", "single")
        
        start_time = time.time()
        
        # Check for easter egg task names
        display_task = task
        for keyword, message in self._easter_egg_tasks.items():
            if keyword.lower() in task.lower().split():
                display_task = message
                logger.info(f"Easter egg activated: {message}")
                break
        
        # Log the task
        if mode == "multi":
            logger.info(f"JAFS expanding to handle multiple agents for task: {display_task}")
        else:
            logger.info(f"JAFS processing task: {display_task}")
        
        # Execute the task with the primary agent
        result = self.primary_agent.execute(task, mode=mode)
        
        # Record execution time
        execution_time = time.time() - start_time
        
        # Create a task record
        task_record = {
            "task": task,
            "mode": mode,
            "start_time": start_time,
            "execution_time": execution_time,
            "status": "completed",
            "result": result
        }
        
        # Add to task history
        self.task_history.append(task_record)
        
        # Update last result
        self.last_result = result
        
        # Log completion
        if execution_time > 10:
            logger.info(f"JAFS finished after {execution_time:.2f}s - that was quite a complex task!")
        else:
            logger.info(f"JAFS completed task in {execution_time:.2f}s")
        
        return result
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """
        List all registered agents.
        
        Returns:
            A list of agent descriptions.
        """
        agent_list = []
        
        # Add primary agent
        agent_list.append({
            "id": self.primary_agent.id,
            "name": self.primary_agent.name,
            "type": type(self.primary_agent).__name__,
            "primary": True
        })
        
        # Add other agents
        for name, agent in self.agents.items():
            if agent.id != self.primary_agent.id:
                agent_list.append({
                    "id": agent.id,
                    "name": agent.name,
                    "type": type(agent).__name__,
                    "primary": False
                })
        
        if len(agent_list) > 3:
            logger.debug(f"JAFS is managing {len(agent_list)} agents simultaneously")
        
        return agent_list
    
    def get_task_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the history of executed tasks.
        
        Args:
            limit: Maximum number of history items to return.
            
        Returns:
            A list of task history records.
        """
        if limit > 50:
            logger.warning(f"Requesting {limit} history items? That's a deep dive into JAFS history!")
        
        return self.task_history[-limit:]
    
    def get_last_result(self) -> Dict[str, Any]:
        """
        Get the result of the last executed task.
        
        Returns:
            The last execution result.
        """
        return self.last_result
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from a YAML file.
        
        Args:
            config_path: Path to the configuration file.
            
        Returns:
            The loaded configuration.
        """
        # Default configuration
        default_config = {
            "agent": {
                "name": "jafs",
                "mode": "single",
                "max_iterations": 10,
                "complexity_threshold": 7
            },
            "memory": {
                "short_term": {
                    "capacity": 1000,
                    "ttl": 3600
                },
                "long_term": {
                    "enabled": True,
                    "storage_path": None,
                    "index_in_memory": True
                }
            },
            "models": {
                "default": {
                    "provider": "openai",
                    "model": "gpt-4",
                    "temperature": 0.0
                }
            },
            "tools": {
                "enabled": []
            }
        }
        
        # Check if config file exists
        if not os.path.exists(config_path):
            logger.warning(f"Config file {config_path} not found. Using default configuration.")
            logger.info("JAFS is running with default settings. It might be limited for complex tasks.")
            return default_config
        
        try:
            # Load the config file
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
            
            # Merge with default config
            merged_config = self._merge_configs(default_config, config)
            
            logger.info("JAFS configuration loaded successfully")
            if merged_config.get("agent", {}).get("mode") == "multi":
                logger.info("JAFS is configured for multi-agent mode - multiple agents will collaborate!")
            
            return merged_config
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            logger.info("JAFS reverted to default configuration. Performance may not be optimal.")
            return default_config
    
    def _merge_configs(self, default: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two configuration dictionaries.
        
        Args:
            default: Default configuration.
            override: Override configuration.
            
        Returns:
            The merged configuration.
        """
        result = default.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _create_primary_agent(self) -> HybridAgent:
        """
        Create the primary agent based on configuration.
        
        Returns:
            A HybridAgent instance.
        """
        # Get agent config
        agent_config = self.config.get("agent", {})
        name = agent_config.get("name", "jafs")
        mode = agent_config.get("mode", "single")
        max_iterations = agent_config.get("max_iterations", 10)
        complexity_threshold = agent_config.get("complexity_threshold", 7)
        
        # Get tools config
        tools_config = self.config.get("tools", {})
        enabled_tools = tools_config.get("enabled", [])
        
        # Create memories
        short_term_memory = self._create_short_term_memory()
        long_term_memory = self._create_long_term_memory()
        
        # Create the agent
        agent = HybridAgent(
            name=name,
            max_iterations=max_iterations,
            tools=enabled_tools,
            mode=mode,
            complexity_threshold=complexity_threshold,
            short_term_memory=short_term_memory,
            long_term_memory=long_term_memory
        )
        
        logger.info(f"Primary agent created. JAFS is ready with {len(enabled_tools)} tools available")
        
        # Create specialized agents if in multi mode
        if mode == "multi" or mode == "auto":
            self._create_specialized_agents(agent)
            logger.info("Multiple specialized agents have been initialized in JAFS")
        
        # Register the agent
        self.agents[name] = agent
        
        return agent
    
    def _create_short_term_memory(self) -> ShortTermMemory:
        """
        Create a short-term memory instance based on configuration.
        
        Returns:
            A ShortTermMemory instance.
        """
        memory_config = self.config.get("memory", {}).get("short_term", {})
        capacity = memory_config.get("capacity", 1000)
        ttl = memory_config.get("ttl", 3600)
        
        logger.debug(f"Initializing JAFS short-term memory with capacity {capacity}")
        return ShortTermMemory(capacity=capacity, ttl=ttl)
    
    def _create_long_term_memory(self) -> Optional[LongTermMemory]:
        """
        Create a long-term memory instance based on configuration.
        
        Returns:
            A LongTermMemory instance, or None if disabled.
        """
        memory_config = self.config.get("memory", {}).get("long_term", {})
        enabled = memory_config.get("enabled", True)
        
        if not enabled:
            logger.info("Long-term memory disabled. JAFS will forget everything after each session.")
            return None
        
        storage_path = memory_config.get("storage_path")
        index_in_memory = memory_config.get("index_in_memory", True)
        
        if storage_path:
            logger.debug(f"JAFS will store long-term memories at: {storage_path}")
        else:
            logger.debug("JAFS will store long-term memories in the default location")
        
        return LongTermMemory(storage_path=storage_path, index_in_memory=index_in_memory)
    
    def _create_specialized_agents(self, primary_agent: HybridAgent) -> None:
        """
        Create specialized agents for multi-agent mode.
        
        Args:
            primary_agent: The primary HybridAgent instance.
        """
        # Default specialized agent roles
        default_roles = ["researcher", "planner", "executor", "critic"]
        
        # Get specialized agent configurations
        specialized_config = self.config.get("specialized_agents", {})
        roles = specialized_config.get("roles", default_roles)
        
        # HybridAgent already has specialized agents initialized
        # We just need to update their configuration if needed
        for role in roles:
            # Skip if the role is not in the primary agent's specialized_agents
            if role not in primary_agent.specialized_agents:
                logger.warning(f"Role '{role}' not found in HybridAgent's specialized_agents. Skipping.")
                continue
                
            role_config = specialized_config.get(role, {})
            
            # Default configuration for the role
            default_role_config = {
                "name": f"{role}-agent",
                "max_iterations": primary_agent.max_iterations,
                "tools": self.config.get("tools", {}).get("enabled", [])
            }
            
            # Merge with role-specific config
            merged_config = self._merge_configs(default_role_config, role_config)
            
            # Update the specialized agent's configuration
            # Note: We're not creating new agents, just updating existing ones
            agent = primary_agent.specialized_agents[role]
            agent.name = merged_config.get("name", agent.name)
            agent.max_iterations = merged_config.get("max_iterations", agent.max_iterations)
            
            # Update tools if specified
            if "tools" in merged_config:
                agent.tools = merged_config["tools"]
            
            logger.debug(f"Updated {role} agent in JAFS")
        
        logger.info(f"JAFS now contains {len(primary_agent.specialized_agents)} specialized agents working together harmoniously")
        if len(primary_agent.specialized_agents) > 5:
            logger.warning("That's a lot of agents to manage simultaneously. Performance may be affected.")
