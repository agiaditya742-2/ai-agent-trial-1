# agent/agent_manager.py

import importlib

class AgentManager:
    """
    Manages the lifecycle of sub-agents.

    This class is responsible for loading and initializing the different agents
    (e.g., ChatAgent, ToolAgent) based on the provided configuration. It acts as a
    central registry for the CoreAgent to access the specialized agents it needs
    to delegate tasks to.
    """

    def __init__(self, agent_configs):
        """
        Initializes the AgentManager and loads all configured agents.

        Args:
            agent_configs (dict): A dictionary where keys are agent names and
                                  values are their configurations (including the
                                  module and class name).
                                  Example:
                                  {
                                      "chat_agent": {
                                          "module": "agents.chat_agent",
                                          "class": "ChatAgent"
                                      },
                                      ...
                                  }
        """
        self.agents = {}
        self._load_agents(agent_configs)

    def _load_agents(self, agent_configs):
        """
        Dynamically imports and instantiates agent classes from the config.

        Args:
            agent_configs (dict): The agent configuration dictionary.
        """
        print("Loading agents...")
        for agent_name, config in agent_configs.items():
            try:
                module_name = config['module']
                class_name = config['class']

                # Dynamically import the module
                agent_module = importlib.import_module(module_name)

                # Get the class from the module
                agent_class = getattr(agent_module, class_name)

                # Instantiate the agent and store it
                self.agents[agent_name] = agent_class()
                print(f"  - Successfully loaded agent: {agent_name}")

            except ImportError as e:
                print(f"Error: Could not import module for agent '{agent_name}'. Details: {e}")
            except AttributeError as e:
                print(f"Error: Could not find class '{config.get('class')}' for agent '{agent_name}'. Details: {e}")
            except Exception as e:
                print(f"An unexpected error occurred while loading agent '{agent_name}'. Details: {e}")
        print("All agents loaded.")

    def get_agent(self, name):
        """
        Retrieves a loaded agent by its name.

        Args:
            name (str): The name of the agent to retrieve.

        Returns:
            object: The agent instance, or None if not found.
        """
        return self.agents.get(name)
