# agent/core_agent.py

import yaml
from agent.agent_manager import AgentManager
from agent.memory import Memory
from agent.personality import Personality
from agent.llm_client import LLMClient

class CoreAgent:
    """
    The central decision-making unit of the AI Agent system, now with a
    reflection step for long-term learning.
    """

    def __init__(self, config_path='config/settings.yaml'):
        self.config = self._load_config(config_path)
        self.memory = Memory(self.config['memory_store_paths'])
        self.personality = Personality(self.config['personality_rules'])
        self.agent_manager = AgentManager(self.config['agent_configs'])
        self.llm_client = LLMClient(api_key=self.config.get('ai_models', {}).get('openai', {}).get('api_key'))

    def _load_config(self, config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def handle_request(self, user_input):
        # 1. Store user input
        self.memory.add_to_short_term({"role": "user", "content": user_input})

        # 2. Determine intent and get a response
        agent_name = self._determine_intent(user_input)
        response = self._execute_agent(agent_name, user_input)

        # 3. Store agent's response
        self.memory.add_to_short_term({"role": "assistant", "content": response})

        # 4. Perform reflection to learn from the interaction
        self._reflect_on_conversation()

        # 5. Save all memory and apply personality
        self.memory.save_memory()
        return self.personality.apply_style(response)

    def _execute_agent(self, agent_name, user_input):
        agent = self.agent_manager.get_agent(agent_name)
        if agent_name == 'chat_agent':
            history = self.memory.get_conversation_history()
            return agent.execute(user_input, conversation_history=history)
        elif agent:
            return agent.execute(user_input)
        else:
            return self.llm_client.generate_response(user_input)

    def _determine_intent(self, user_input):
        if "weather" in user_input.lower() or "time" in user_input.lower() or "date" in user_input.lower():
            return "tool_agent"
        elif "remind me" in user_input.lower() or "task" in user_input.lower():
            return "task_agent"
        else:
            return "chat_agent"

    def _reflect_on_conversation(self):
        """
        Analyzes the recent conversation to extract key facts for long-term memory.
        """
        print("[CoreAgent] Reflecting on the conversation...")
        history = self.memory.get_conversation_history()

        # Don't reflect on very short conversations
        if len(history) < 2:
            print("[CoreAgent] Not enough history to reflect.")
            return

        # Create a prompt for the LLM to extract key facts
        prompt = f"""
        Based on the following conversation history, what are the key facts to remember about the user?
        Facts could include their name, preferences, goals, or any other important information.
        Format the facts as a JSON list of strings. For example: ["The user's name is John.", "The user likes dogs."]
        If there are no new key facts, respond with an empty list [].

        Conversation:
        {history}
        """

        # Use the LLM to extract facts (in simulation mode, this will be a placeholder)
        extracted_facts = self.llm_client.generate_response(prompt)

        try:
            # In a real scenario, we'd parse the JSON from the LLM.
            # For simulation, we'll check for a specific phrase.
            if "my name is" in str(history).lower():
                user_name = "User" # Default
                for msg in history:
                    if "my name is" in msg.get('content', '').lower():
                        user_name = msg['content'].lower().split("my name is")[-1].strip().capitalize()

                fact = f"The user's name is {user_name}."
                print(f"[CoreAgent] Learned a new fact: {fact}")
                self.memory.add_to_long_term({"fact": fact})

        except Exception as e:
            print(f"Error during reflection: {e}")
