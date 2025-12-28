# agent/agent_manager.py

import importlib
import logging
from typing import Dict, Any, List

# Configure logging for this module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - (AgentManager) - %(message)s')

class AgentManager:
    """
    Manages the lifecycle and orchestration of sub-agents.

    This class is responsible for dynamically loading, initializing, and providing
    access to the various specialized agents defined in the configuration. It acts
    as a central nervous system for the CoreAgent, allowing it to delegate tasks
    efficiently and understand the capabilities of its sub-components.
    """

    def __init__(self, agent_configs: Dict[str, Any]):
        """
        Initializes the AgentManager and loads all configured agents.

        Args:
            agent_configs (dict): A dictionary defining the agents to be loaded.
        """
        self.agents: Dict[str, Any] = {}
        self.agent_capabilities: Dict[str, str] = {}
        if agent_configs:
            self._load_agents(agent_configs)
        else:
            logging.warning("No agent configurations provided. AgentManager will be empty.")

    def _load_agents(self, agent_configs: Dict[str, Any]):
        """
        Dynamically imports and instantiates agent classes from the configuration.
        This method is designed to be resilient, logging errors for individual
        agent failures without crashing the entire system.
        """
        logging.info("Starting to load agents...")
        for agent_name, config in agent_configs.items():
            if not config.get('enabled', False):
                logging.info(f"Skipping disabled agent: {agent_name}")
                continue

            try:
                module_name = config.get('module')
                class_name = config.get('class')

                if not module_name or not class_name:
                    raise ValueError("'module' and 'class' must be defined in agent config.")

                # Dynamically import the module
                agent_module = importlib.import_module(module_name)

                # Get the class from the module
                agent_class = getattr(agent_module, class_name)

                # Instantiate the agent and store it
                self.agents[agent_name] = agent_class()

                # Store agent capabilities if provided in the class docstring
                self.agent_capabilities[agent_name] = agent_class.__doc__.strip().split('\n')[0]

                logging.info(f"Successfully loaded and initialized agent: '{agent_name}'")

            except ImportError as e:
                logging.error(f"ModuleImportError for agent '{agent_name}'. Module: '{config.get('module')}'. Details: {e}")
            except AttributeError as e:
                logging.error(f"ClassNotFoundError for agent '{agent_name}'. Class: '{config.get('class')}'. Details: {e}")
            except ValueError as e:
                logging.error(f"ConfigurationError for agent '{agent_name}'. Details: {e}")
            except Exception as e:
                logging.error(f"An unexpected error occurred while loading agent '{agent_name}'. Details: {e}")

        logging.info("Agent loading process complete.")

    def get_agent(self, name: str) -> Any:
        """
        Retrieves a loaded agent by its name.

        Args:
            name (str): The name of the agent to retrieve.

        Returns:
            An agent instance, or None if the agent is not found or failed to load.
        """
        agent_instance = self.agents.get(name)
        if not agent_instance:
            logging.warning(f"Attempted to access non-existent or failed agent: '{name}'")
        return agent_instance

    def list_agents(self) -> List[str]:
        """
        Returns a list of all successfully loaded agent names.
        """
        return list(self.agents.keys())

    def get_all_capabilities(self) -> Dict[str, str]:
        """
        Returns a dictionary mapping agent names to their capabilities.
        """
        return self.agent_capabilities

if __name__ == '__main__':
    print("--- Testing Expanded AgentManager ---")

    sample_config = {
        "chat_agent": {
            "module": "agents.chat_agent",
            "class": "ChatAgent",
            "enabled": True
        },
        "tool_agent": {
            "module": "agents.tool_agent",
            "class": "ToolAgent",
            "enabled": True
        },
        "disabled_agent": {
            "module": "some.fake.module",
            "class": "FakeAgent",
            "enabled": False
        },
        "bad_config_agent": {
            "module": "agents.task_agent",
            "enabled": True
            # Missing "class"
        }
    }

    # 1. Initialize manager
    manager = AgentManager(sample_config)
    print("\n[1] AgentManager initialized.")

    # 2. List loaded agents
    loaded_agents = manager.list_agents()
    print(f"\n[2] Loaded agents: {loaded_agents}")
    assert "chat_agent" in loaded_agents
    assert "tool_agent" in loaded_agents
    assert "disabled_agent" not in loaded_agents
    assert "bad_config_agent" not in loaded_agents

    # 3. Get a specific agent
    chat_agent_instance = manager.get_agent("chat_agent")
    print(f"\n[3] Retrieved chat_agent: {'Success' if chat_agent_instance else 'Failure'}")
    assert chat_agent_instance is not None

    # 4. Get capabilities
    capabilities = manager.get_all_capabilities()
    print("\n[4] Agent Capabilities:")
    for name, desc in capabilities.items():
        print(f"  - {name}: {desc}")
    assert "chat_agent" in capabilities

    print("\n--- AgentManager Test Complete ---")
