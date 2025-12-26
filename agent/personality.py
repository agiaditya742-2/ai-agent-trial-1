# agent/personality.py

class Personality:
    """
    Manages the agent's communication style based on dynamic profiles.

    This class loads a set of personality profiles from the configuration
    and uses the active profile to shape the agent's responses. This allows
    the agent's tone (e.g., friendly, formal) to be changed easily.
    """

    def __init__(self, rules):
        """
        Initializes the Personality class with a set of rules and profiles.

        Args:
            rules (dict): A dictionary containing personality rules, including
                          the active profile and a dictionary of profiles.
        """
        self.active_profile_name = rules.get("active_profile", "friendly")
        self.profiles = rules.get("profiles", {})
        self.active_profile = self.profiles.get(self.active_profile_name, {})

    def get_response(self, response_type):
        """
        Retrieves a standard response from the active personality profile.

        Args:
            response_type (str): The type of response (e.g., "greeting").

        Returns:
            str: The predefined response, or a default message.
        """
        return self.active_profile.get("standard_responses", {}).get(response_type, "...")

    def apply_style(self, text):
        """
        Applies the active personality's style to a given text.

        Args:
            text (str): The text to be styled.

        Returns:
            str: The styled text.
        """
        prefix = self.active_profile.get("style_prefix", "")
        return f"{prefix}{text}"

if __name__ == '__main__':
    # Example usage for testing the Personality class

    sample_rules = {
        "active_profile": "formal",
        "profiles": {
            "friendly": {
                "style_prefix": "Hey, AI here: ",
                "standard_responses": {"greeting": "What's up?"}
            },
            "formal": {
                "style_prefix": "AI Unit 734: ",
                "standard_responses": {"greeting": "Greetings."}
            }
        }
    }

    # 1. Initialize with the sample rules
    personality = Personality(sample_rules)
    print(f"Active Profile: {personality.active_profile_name}")

    # 2. Test getting a standard response from the active (formal) profile
    print(f"Greeting: {personality.get_response('greeting')}")

    # 3. Test applying the style of the active (formal) profile
    styled_message = personality.apply_style("The operation was a success.")
    print(f"Styled Message: {styled_message}")

    # 4. Switch to the friendly profile to test dynamic loading
    sample_rules['active_profile'] = 'friendly'
    friendly_personality = Personality(sample_rules)
    print(f"\nActive Profile: {friendly_personality.active_profile_name}")
    print(f"Greeting: {friendly_personality.get_response('greeting')}")
    friendly_styled = friendly_personality.apply_style("Let's get this party started.")
    print(f"Styled Message: {friendly_styled}")
