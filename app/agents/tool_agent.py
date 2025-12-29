
from app.tools import api_tools, system_tools
import json

class ToolAgent:
    def __init__(self):
        """Initializes the ToolAgent by mapping tool names to functions."""
        self.tools = {
            # API Tools
            "search_internet": api_tools.search_internet,

            # System Tools
            "create_file": system_tools.create_file,
            "read_file": system_tools.read_file,
            "list_files": system_tools.list_files,
        }

    def use_tool(self, tool_name: str, **kwargs):
        """
        Executes a specified tool with given arguments.

        Args:
            tool_name (str): The name of the tool to execute.
            **kwargs: Keyword arguments for the tool function.

        Returns:
            str: A JSON string containing the result of the tool execution.
        """
        if tool_name in self.tools:
            try:
                # Execute the corresponding function
                result = self.tools[tool_name](**kwargs)
                return result
            except Exception as e:
                error_message = f"An error occurred while using the tool '{tool_name}': {str(e)}"
                return json.dumps({"status": "error", "message": error_message})
        else:
            return json.dumps({"status": "error", "message": f"Tool '{tool_name}' is not available."})
