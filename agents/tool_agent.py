# agents/tool_agent.py

import logging
from typing import Dict, Any

from tools.api_tools import ApiTools
from tools.system_tools import SystemTools
from tools.desktop_tools import DesktopTools
from tools.internet_tools import search_web, read_website_content

# Configure logging for this module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - (ToolAgent) - %(message)s')

class ToolAgent:
    """
    Handles the execution of a wide array of tools, from APIs to desktop actions.
    """

    def __init__(self, external_api_config: Dict[str, Any] = None):
        """
        Initializes the ToolAgent with its available toolsets.
        """
        self.api_tools = ApiTools()
        self.system_tools = SystemTools()
        self.desktop_tools = DesktopTools()
        self.external_api_config = external_api_config or {}

    def execute(self, user_input: str) -> Dict[str, Any]:
        """
        Parses the user's request and executes the most appropriate tool.
        This method acts as a sophisticated router, using keyword matching and
        context analysis to select and execute the correct tool function.

        Args:
            user_input (str): The task to be performed by a tool.

        Returns:
            A dictionary containing the result and status of the operation.
        """
        logging.info(f"Processing tool request: '{user_input}'")

        # --- Routing Logic ---
        # The routing is ordered from most specific to most general commands.

        try:
            # Desktop Tools
            if "open" in user_input.lower():
                app_name = user_input.split("open", 1)[1].strip()
                result = self.desktop_tools.open_application(app_name)
                return self._format_response(result, "desktop_tools")

            # Internet Tools
            if "search for" in user_input.lower():
                query = user_input.split("search for", 1)[1].strip()
                search_config = self.external_api_config.get('google_search', {})
                result = search_web(query, search_config.get('api_key'), search_config.get('search_engine_id'))
                return self._format_response(result, "internet_tools")

            # System Tools
            if any(kw in user_input.lower() for kw in ["what time is it", "current time"]):
                result = self.system_tools.get_current_time()
                return self._format_response(result, "system_tools")

            # API Tools
            if "weather in" in user_input.lower():
                city = user_input.split("weather in", 1)[1].strip().replace("?", "")
                result = self.api_tools.get_weather(city)
                return self._format_response(result, "api_tools")

            # Default case if no tool matches
            logging.warning(f"No specific tool found for input: '{user_input}'")
            return self._format_response("I'm sorry, I don't have a tool that can handle that specific request.", "ToolAgent", "failed")

        except Exception as e:
            logging.error(f"An error occurred while executing a tool for input '{user_input}': {e}")
            return self._format_response(f"An internal error occurred while using a tool. Details: {e}", "ToolAgent", "error")

    def _format_response(self, result: str, tool_used: str, status: str = "success") -> Dict[str, Any]:
        """
        Formats the tool's output into a structured dictionary.
        """
        return {
            "status": status,
            "tool_used": tool_used,
            "result": result
        }

if __name__ == '__main__':
    print("--- Testing Expanded ToolAgent ---")
    tool_agent = ToolAgent()

    test_cases = [
        "open VS Code",
        "what time is it",
        "what is the weather in London?",
        "search for the capital of France",
        "tell me a joke" # Should fail gracefully
    ]

    for case in test_cases:
        print(f"\nInput: '{case}'")
        response = tool_agent.execute(case)
        print(f"Response: {response}")
        assert "status" in response
        assert "result" in response

    print("\n--- ToolAgent Test Complete ---")
