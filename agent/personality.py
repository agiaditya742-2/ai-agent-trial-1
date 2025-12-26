# agent/personality.py

class Personality:
    """
    Manages the agent's communication style and response rules.

    This class uses a set of rules defined in the configuration to shape the
    agent's responses. It can provide standard replies (like greetings) and
    apply stylistic modifications to any given text to make it sound more
    like the agent's defined character.
    """

    def __init__(self, rules):
        """
        Initializes the Personality class with a set of rules.

        Args:
            rules (dict): A dictionary containing personality rules, such as
                          standard responses and stylistic prefixes.
                          Example:
                          {
                              "standard_responses": {
                                  "greeting": "Hello! How can I help you?",
                                  "farewell": "Goodbye! Have a great day."
                              },
                              "style_prefix": "As an AI assistant, I can say: "
                          }
        """
        self.rules = rules

    def get_response(self, response_type):
        """
        Retrieves a standard response from the personality rules.

        Args:
            response_type (str): The type of response to retrieve (e.g., "greeting").

        Returns:
            str: The predefined response, or a default message if not found.
        """
        return self.rules.get("standard_responses", {}).get(response_type, "...")

    def apply_style(self, text):
        """
        Applies the agent's personality style to a given text.

        For example, it might add a prefix to every response to make it sound
        more formal or robotic.

        Args:
            text (str): The text to be styled.

        Returns:
            str: The text with the personality style applied.
        """
        prefix = self.rules.get("style_prefix", "")
        return f"{prefix}{text}"

if __name__ == '__main__':
    # Example usage for testing the Personality class

    # Define some sample personality rules
    sample_rules = {
        "standard_responses": {
            "greeting": "Greetings, human. I am ready to assist.",
            "farewell": "Mission complete. Powering down."
        },
        "style_prefix": "AI says: "
    }

    # Create an instance of the Personality class
    personality = Personality(sample_rules)

    # Test getting standard responses
    print(f"Greeting: {personality.get_response('greeting')}")
    print(f"Farewell: {personality.get_response('farewell')}")

    # Test applying style to a custom message
    custom_message = "The sky is blue."
    styled_message = personality.apply_style(custom_message)
    print(f"Styled Message: {styled_message}")
