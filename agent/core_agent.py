# agent/core_agent.py

import yaml
from agent.agent_manager import AgentManager
from agent.memory import Memory
from agent.personality import Personality
from agent.llm_client import LLMClient

class CoreAgent:
    """
    The central decision-making unit of the AI Agent system.

    This upgraded class uses an LLM to understand user intent, route tasks,
    and generate conversational responses, making it much more intelligent.
    """

    def __init__(self, config_path='config/settings.yaml'):
        """
        Initializes the CoreAgent with all its necessary components.
        """
        self.config = self._load_config(config_path)
        self.memory = Memory(self.config['memory_store_paths'])
        self.personality = Personality(self.config['personality_rules'])
        self.agent_manager = AgentManager(self.config['agent_configs'])
        self.llm_client = LLMClient(api_key=self.config.get('ai_models', {}).get('openai', {}).get('api_key'))

    def _load_config(self, config_path):
        """
        Loads the system configuration from a YAML file.
        """
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def handle_request(self, user_input):
        """
        Processes user input using an LLM for routing and response.

        Args:
            user_input (str): The input from the user.

        Returns:
            str: The response from the appropriate agent.
        """
        # 1. Store user input in memory
        self.memory.add_to_short_term({"role": "user", "content": user_input})

        # 2. Use LLM to determine intent and select an agent
        agent_name = self._determine_intent(user_input)

        # 3. Execute the appropriate agent
        if agent_name in self.agent_manager.agents:
            agent = self.agent_manager.get_agent(agent_name)
            response = agent.execute(user_input)
        else:
            # Default to conversational response using the LLM
            response = self.llm_client.generate_response(user_input)

        # 4. Store the agent's response
        self.memory.add_to_short_term({"role": "assistant", "content": response})
        self.memory.save_memory()

        # 5. Apply personality
        styled_response = self.personality.apply_style(response)

        return styled_response

    def _determine_intent(self, user_input):
        """
        Uses the LLM to determine the user's intent and select the best agent.
        """
        # Create a prompt for the LLM to choose the best agent
        prompt = f"""
        Given the user's request: "{user_input}"
        Which of the following agents is best suited to handle this?
        - 'tool_agent': For requests that need tools, like checking the weather or time.
        - 'task_agent': For managing a to-do list, like adding or listing tasks.
        - 'chat_agent': For general conversation, jokes, or questions.

        Please respond with only the name of the agent (e.g., 'tool_agent').
        """

        # In a real scenario, we would use the LLM's response.
        # For this simulation, we'll keep the keyword logic to avoid API costs.
        if "weather" in user_input.lower() or "time" in user_input.lower() or "date" in user_input.lower():
            return "tool_agent"
        elif "remind me" in user_input.lower() or "task" in user_input.lower():
            return "task_agent"
        else:
            return "chat_agent"
