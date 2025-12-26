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

if __name__ == '__main__':
    # This block is for testing the AgentManager directly.
    # It requires the agent modules to exist to work correctly.

    # Create dummy agent files for testing
    import os
    if not os.path.exists('agents'):
        os.makedirs('agents')

    with open('agents/test_chat_agent.py', 'w') as f:
        f.write("""
class TestChatAgent:
    def execute(self, task):
        return f"Chatting about: {task}"
""")

    with open('agents/test_tool_agent.py', 'w') as f:
        f.write("""
class TestToolAgent:
    def execute(self, task):
        return f"Using tools for: {task}"
""")
    # Need to add empty __init__.py for imports to work
    with open('agents/__init__.py', 'w') as f:
        pass


    # Define a sample configuration
    sample_agent_configs = {
        "chat_agent": {
            "module": "agents.test_chat_agent",
            "class": "TestChatAgent"
        },
        "tool_agent": {
            "module": "agents.test_tool_agent",
            "class": "TestToolAgent"
        }
    }

    # 1. Initialize the AgentManager
    manager = AgentManager(sample_agent_configs)

    # 2. Get a specific agent
    chat_agent = manager.get_agent("chat_agent")
    if chat_agent:
        print(f"\nRetrieved chat_agent: {chat_agent}")
        # 3. Execute a task with the agent
        response = chat_agent.execute("the weather")
        print(f"Response from chat_agent: {response}")
    else:
        print("Could not retrieve chat_agent.")

    tool_agent = manager.get_agent("tool_agent")
    if tool_agent:
        print(f"\nRetrieved tool_agent: {tool_agent}")
        response = tool_agent.execute("checking the time")
        print(f"Response from tool_agent: {response}")
    else:
        print("Could not retrieve tool_agent.")

    # Clean up the dummy files
    os.remove('agents/test_chat_agent.py')
    os.remove('agents/test_tool_agent.py')
    os.remove('agents/__init__.py')
