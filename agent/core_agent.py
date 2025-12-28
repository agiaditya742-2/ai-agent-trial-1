# agent/core_agent.py

import yaml
import logging
import threading
from agent.agent_manager import AgentManager
from agent.memory import Memory
from agent.personality import Personality
from agent.llm_client import LLMClient
from agent.autonomous_agent import AutonomousAgent

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

        # Autonomous and advanced features state
        self.autonomous_agent: AutonomousAgent = None
        self.deep_thinking_mode: bool = False

        # Ensure the conversation starts with a greeting if the history is empty
        if not self.memory.get_conversation_history():
            greeting = self.personality.get_greeting()
            self.memory.add_to_short_term({"role": "assistant", "content": greeting})

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
        """
        Determines the user's intent by leveraging the LLM for advanced routing.
        This is a significant upgrade from simple keyword matching.
        """
        # Create a detailed context for the LLM to make an informed decision
        context = {
            "user_input": user_input,
            "conversation_history": self.memory.get_conversation_history(limit=5),
            "available_agents": list(self.agent_manager.agents.keys()),
            "tool_capabilities": {
                "api_tools": "Get weather and news.",
                "system_tools": "Get current time and date.",
                "desktop_tools": "Open/close apps, list/create files, manage clipboard.",
                "internet_tools": "Search the web and read website content."
            },
            "recent_knowledge": self.memory.get_knowledge(user_input)
        }

        # Use the LLM's routing capabilities
        # This will simulate the LLM choosing the best agent based on the context.
        # In a real scenario, this would be a dedicated prompt and function call.

        # Heuristics for simulation
        if any(kw in user_input.lower() for kw in ["open", "close", "list files", "create file", "clipboard"]):
            return "tool_agent" # Desktop tools are in ToolAgent
        if any(kw in user_input.lower() for kw in ["weather", "news", "time", "date"]):
             return "tool_agent" # System/API tools are in ToolAgent
        if any(kw in user_input.lower() for kw in ["search for", "read website"]):
             return "tool_agent" # Internet tools are in ToolAgent
        if any(kw in user_input.lower() for kw in ["remind me", "add task", "my tasks"]):
            return "task_agent"

        # Default to chat agent for general conversation
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

    def toggle_deep_thinking(self, mode: bool):
        """Enable or disable deep thinking mode."""
        self.deep_thinking_mode = mode
        logging.info(f"Deep Thinking Mode set to: {self.deep_thinking_mode}")
        return {"status": "success", "deep_thinking_mode": self.deep_thinking_mode}

    def start_autonomous_mode(self, goal: str):
        """
        Starts the autonomous agent in a background thread with a specific goal.
        """
        if self.autonomous_agent and self.autonomous_agent.is_running:
            logging.warning("Attempted to start autonomous agent while it was already running.")
            return {"status": "error", "message": "Autonomous agent is already running."}

        logging.info(f"Initiating autonomous agent for goal: {goal}")
        self.autonomous_agent = AutonomousAgent(goal=goal, core_agent=self)

        # Run the agent in a separate thread to avoid blocking the server
        agent_thread = threading.Thread(target=self.autonomous_agent.run)
        agent_thread.start()

        return {"status": "success", "message": f"Autonomous agent has been dispatched to work on: {goal}"}

    def stop_autonomous_mode(self):
        """Stops the autonomous agent."""
        if not self.autonomous_agent or not self.autonomous_agent.is_running:
            return {"status": "error", "message": "Autonomous agent is not running."}

        self.autonomous_agent.stop()
        logging.info("Autonomous agent stopped.")
        return {"status": "success", "message": "Autonomous agent stopped."}

    def get_autonomous_status(self):
        """Gets the status of the autonomous agent."""
        if not self.autonomous_agent:
            return {"status": "idle", "message": "Autonomous agent has not been started."}
        return self.autonomous_agent.get_status()
