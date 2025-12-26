# agent/core_agent.py

import yaml
from agent.agent_manager import AgentManager
from agent.memory import Memory
from agent.personality import Personality

class CoreAgent:
    """
    The central decision-making unit of the AI Agent system.

    This class is responsible for orchestrating the different components of the agent,
    including memory, personality, and sub-agent management. It receives user input,
    determines the appropriate agent to handle the request, and returns the
    final response.
    """

    def __init__(self, config_path='config/settings.yaml'):
        """
        Initializes the CoreAgent with all its necessary components.

        Args:
            config_path (str): The path to the configuration file.
        """
        self.config = self._load_config(config_path)
        self.memory = Memory(self.config['memory_store_paths'])
        self.personality = Personality(self.config['personality_rules'])
        self.agent_manager = AgentManager(self.config['agent_configs'])
        self.is_running = True

    def _load_config(self, config_path):
        """
        Loads the system configuration from a YAML file.

        Args:
            config_path (str): The path to the settings.yaml file.

        Returns:
            dict: The configuration settings.
        """
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file not found at {config_path}.")
            # Provide a default or exit
            return {}
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            return {}

    def start(self):
        """
        Starts the main loop of the agent.
        """
        print(self.personality.get_response("greeting"))
        while self.is_running:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                self.stop()
            else:
                response = self.handle_request(user_input)
                print(f"Agent: {response}")

    def stop(self):
        """
        Stops the agent and saves memory.
        """
        print(self.personality.get_response("farewell"))
        self.memory.save_memory()
        self.is_running = False

    def handle_request(self, user_input):
        """
        Processes user input and routes it to the appropriate agent.

        Args:
            user_input (str): The input from the user.

        Returns:
            str: The response from the appropriate agent.
        """
        # 1. Store user input in short-term memory
        self.memory.add_to_short_term({"role": "user", "content": user_input})

        # 2. Determine the user's intent and select an agent
        # (This is a simplified routing logic. A real implementation would use an LLM for this)
        if "what time is it" in user_input.lower():
            agent_name = "tool_agent"
        elif "tell me a joke" in user_input.lower():
            agent_name = "chat_agent"
        elif "remind me to" in user_input.lower() or "what are my tasks" in user_input.lower() or "list tasks" in user_input.lower():
            agent_name = "task_agent"
        else:
            agent_name = "chat_agent"  # Default agent

        # 3. Get the appropriate agent and execute the task
        agent = self.agent_manager.get_agent(agent_name)
        if agent:
            response = agent.execute(user_input)
        else:
            response = "I don't know how to handle that request."

        # 4. Store the agent's response in short-term memory
        self.memory.add_to_short_term({"role": "assistant", "content": response})

        # 5. Apply personality to the response
        styled_response = self.personality.apply_style(response)

        return styled_response

if __name__ == '__main__':
    # This is for testing the CoreAgent directly
    core_agent = CoreAgent()
    core_agent.start()
