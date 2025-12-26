# agent/llm_client.py

import os
import httpx
from openai import OpenAI

class LLMClient:
    """
    A client for interacting with a Large Language Model (LLM) like OpenAI's GPT.

    This class centralizes the logic for sending requests to the LLM and
    handling the responses. It is designed to be used by other components of
    the agent system that require natural language understanding or generation.
    """

    def __init__(self, api_key=None):
        """
        Initializes the LLMClient.

        Args:
            api_key (str, optional): The API key for the LLM service. If not
                                     provided, it will look for the
                                     OPENAI_API_KEY environment variable.
                                     Defaults to "YOUR_API_KEY_HERE" if neither
                                     is found.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "YOUR_API_KEY_HERE")

        self.client = None
        if self.api_key and self.api_key != "YOUR_API_KEY_HERE":
            try:
                # Create a custom httpx client that ignores system proxies
                http_client = httpx.Client(proxies={})
                self.client = OpenAI(api_key=self.api_key, http_client=http_client)
            except Exception as e:
                print(f"Error initializing OpenAI client: {e}. Running in simulation mode.")
        else:
            print("Warning: OpenAI API key is not set. Using simulation mode.")

    def generate_response(self, prompt, model="gpt-3.5-turbo"):
        """
        Generates a response from the LLM based on a given prompt.

        Args:
            prompt (str): The input prompt to send to the LLM.
            model (str): The model to use for the generation.

        Returns:
            str: The LLM's generated response.
        """
        if not self.client:
            return self._simulate_response(prompt)

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"An error occurred while communicating with the LLM: {e}")
            return "Sorry, I'm having trouble connecting to the AI model right now."

    def _simulate_response(self, prompt):
        """
        Simulates an LLM response for when no API key is provided.

        Args:
            prompt (str): The input prompt.

        Returns:
            str: A simulated response.
        """
        if "joke" in prompt.lower():
            return "This is a simulated joke."
        elif "time" in prompt.lower():
            return "This is a simulated time."
        else:
            return "This is a simulated response to your prompt."

if __name__ == '__main__':
    # Example usage for testing the LLMClient

    # To test with a real API key, you can set it as an environment variable:
    # export OPENAI_API_KEY='your-real-api-key'

    # 1. Test in simulation mode (no API key)
    print("--- Testing in Simulation Mode ---")
    llm_client_simulated = LLMClient()
    simulated_response = llm_client_simulated.generate_response("Tell me a joke about computers.")
    print(f"Prompt: 'Tell me a joke about computers.'\nResponse: '{simulated_response}'\n")

    # 2. Test with a placeholder API key (will also use simulation)
    print("--- Testing with Placeholder API Key ---")
    llm_client_placeholder = LLMClient(api_key="YOUR_API_KEY_HERE")
    placeholder_response = llm_client_placeholder.generate_response("What time is it?")
    print(f"Prompt: 'What time is it?'\nResponse: '{placeholder_response}'\n")

    # 3. Test with a fake API key to demonstrate error handling
    # (This will likely fail and print an error message, which is expected)
    print("--- Testing with a Fake API Key (Expect an Error) ---")
    llm_client_fake = LLMClient(api_key="fake-key")
    fake_response = llm_client_fake.generate_response("Any prompt")
    print(f"Prompt: 'Any prompt'\nResponse: '{fake_response}'\n")
