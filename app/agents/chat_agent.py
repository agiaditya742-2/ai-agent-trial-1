
from app.agent.personality import Personality

class ChatAgent:
    def __init__(self, personality: Personality):
        """
        Initializes the ChatAgent with a given personality.

        Args:
            personality (Personality): The personality configuration for the agent.
        """
        self.personality = personality

    def get_response(self, user_input: str) -> str:
        """
        Generates a simple, rule-based response for conversational input.
        """
        # This is a basic placeholder. A real implementation would use an LLM.
        response = f"{self.personality.get_name()}: You said '{user_input}'. How can I help you?"
        return response
