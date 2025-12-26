# agents/tool_agent.py

from tools.api_tools import ApiTools
from tools.system_tools import SystemTools

class ToolAgent:
    """
    Handles the execution of tools and APIs.

    This agent acts as a router, determining which tool is best suited to handle
    a user's request. It uses instances of tool collections (like ApiTools and
    SystemTools) to perform the actual operations.

    The logic for selecting a tool is currently based on simple keyword matching.
    In a more advanced system, this would be replaced by an LLM-based tool
    selection model that can better understand the user's intent.
    """

    def __init__(self):
        """
        Initializes the ToolAgent with its available toolsets.
        """
        self.api_tools = ApiTools()
        self.system_tools = SystemTools()

    def execute(self, user_input):
        """
        Parses the user's request and executes the appropriate tool.

        Args:
            user_input (str): The task to be performed by a tool.

        Returns:
            str: The result from the executed tool, or an error message.
        """
        print(f"[ToolAgent] Processing input: '{user_input}'")

        # Simplified routing logic to select the right tool
        if "weather" in user_input.lower():
            # A more robust way to find the city name
            parts = user_input.lower().split(" in ")
            if len(parts) > 1:
                city = parts[1].strip().replace("?", "")
                return self.api_tools.get_weather(city)
            else:
                return "Please specify a city, for example: 'what is the weather in New York?'"

        elif "news" in user_input.lower():
            # Example: "get today's news"
            return self.api_tools.get_news()

        elif "time" in user_input.lower():
            # Example: "what time is it?"
            return self.system_tools.get_current_time()

        elif "date" in user_input.lower():
            # Example: "what is today's date?"
            return self.system_tools.get_current_date()

        else:
            return "I don't have a tool for that task."
