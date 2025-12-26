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
            # Example: "what is the weather in London?"
            city = user_input.lower().split("in ")[-1]
            return self.api_tools.get_weather(city)

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

if __name__ == '__main__':
    # Example usage for testing the ToolAgent directly

    # We need to create dummy tool modules and classes for this test to run
    import os
    if not os.path.exists('tools'):
        os.makedirs('tools')

    # Dummy ApiTools
    with open('tools/api_tools.py', 'w') as f:
        f.write("""
class ApiTools:
    def get_weather(self, city):
        return f"Fetching weather for {city}... It is sunny."
    def get_news(self):
        return "Fetching news... AI agents are taking over!"
""")

    # Dummy SystemTools
    with open('tools/system_tools.py', 'w') as f:
        f.write("""
import datetime
class SystemTools:
    def get_current_time(self):
        return f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}."
    def get_current_date(self):
        return f"Today's date is {datetime.datetime.now().strftime('%Y-%m-%d')}."
""")
    with open('tools/__init__.py', 'w') as f:
        pass

    # Now we can initialize and test the ToolAgent
    tool_agent = ToolAgent()

    # Test cases
    print(f"Request: 'what is the weather in new york?'\nResponse: {tool_agent.execute('what is the weather in new york?')}\n")
    print(f"Request: 'get the latest news'\nResponse: {tool_agent.execute('get the latest news')}\n")
    print(f"Request: 'what time is it now?'\nResponse: {tool_agent.execute('what time is it now?')}\n")
    print(f"Request: 'tell me the date'\nResponse: {tool_agent.execute('tell me the date')}\n")
    print(f"Request: 'tell me a story'\nResponse: {tool_agent.execute('tell me a story')}\n")

    # Clean up dummy files
    os.remove('tools/api_tools.py')
    os.remove('tools/system_tools.py')
    os.remove('tools/__init__.py')
