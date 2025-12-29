
from app.agent.personality import Personality
from app.agent.memory import Memory
from app.agents.chat_agent import ChatAgent
from app.agents.tool_agent import ToolAgent
import re
import json

class CoreAgent:
    def __init__(self, memory: Memory):
        """
        Initializes the CoreAgent.

        Args:
            memory (Memory): The memory system for the agent.
        """
        self.personality = Personality(config_file='app/config/settings.yaml')
        self.memory = memory
        self.chat_agent = ChatAgent(self.personality)
        self.tool_agent = ToolAgent()

    def process(self, user_input: str) -> str:
        """
        Processes user input, routes to the appropriate sub-agent, and returns the response.

        This version can now handle both regular chat and specific tool commands.
        A tool command is expected in a format like:
        "TOOL: use_tool_name(param1='value1', param2='value2')"
        """
        self.memory.add_to_short_term(f"user: {user_input}")

        # Check if the input is a tool command
        if user_input.strip().upper().startswith("TOOL:"):
            command_str = user_input.strip()[5:].strip() # Extract the command part

            # Use regex to parse the tool name and arguments
            match = re.match(r"(\w+)\((.*)\)", command_str)
            if match:
                tool_name = match.group(1)
                args_str = match.group(2)

                try:
                    # Convert string arguments to a dictionary
                    # Note: This is a simplified parser. For production, a more robust solution
                    # like ast.literal_eval would be safer.
                    kwargs = dict(arg.split('=') for arg in args_str.split(', '))
                    # Clean up quotes from values
                    for key, value in kwargs.items():
                        kwargs[key] = value.strip("'\"")

                    # Use the tool agent
                    response = self.tool_agent.use_tool(tool_name, **kwargs)
                except Exception as e:
                    response = json.dumps({"status": "error", "message": f"Failed to parse or execute tool command: {str(e)}"})
            else:
                response = json.dumps({"status": "error", "message": "Invalid tool command format."})
        else:
            # Default to chat agent for conversational input
            response = self.chat_agent.get_response(user_input)

        self.memory.add_to_short_term(f"agent: {response}")
        return response
