# agent/personality.py

import random
from typing import Dict, Any

class Personality:
    """
    Manages the agent's personality, including its style of communication,
    moods, and response templates. This allows the agent to have a more
    dynamic and engaging character.
    """

    def __init__(self, personality_rules: Dict[str, Any]):
        """
        Initializes the Personality class with a set of rules from the config.

        Args:
            personality_rules (dict): A dictionary containing personality profiles and settings.
        """
        self.profiles = personality_rules.get('profiles', {})
        self.default_profile = personality_rules.get('default', 'neutral')
        self.current_profile_name = self.default_profile
        self.current_profile = self.profiles.get(self.current_profile_name, {})

    def set_profile(self, profile_name: str) -> bool:
        """
        Sets the agent's active personality profile.

        Args:
            profile_name (str): The name of the profile to activate.

        Returns:
            bool: True if the profile was successfully set, False otherwise.
        """
        if profile_name in self.profiles:
            self.current_profile_name = profile_name
            self.current_profile = self.profiles[profile_name]
            print(f"Personality profile set to '{profile_name}'.")
            return True
        print(f"Warning: Personality profile '{profile_name}' not found.")
        return False

    def get_greeting(self) -> str:
        """Returns a greeting based on the current personality profile."""
        greetings = self.current_profile.get('greetings', ["Hello.", "Hi there."])
        return random.choice(greetings)

    def get_farewell(self) -> str:
        """Returns a farewell based on the current personality profile."""
        farewells = self.current_profile.get('farewells', ["Goodbye.", "Bye."])
        return random.choice(farewells)

    def apply_style(self, response: str) -> str:
        """
        Applies the current personality's style to a given response.
        This can include adding intros, outros, or modifying wording.
        """
        intro = random.choice(self.current_profile.get('response_intros', ["", "Well, ", "I think, "]))
        outro = random.choice(self.current_profile.get('response_outros', ["", "...", "!", "."]))

        # This is a simple implementation. A more advanced version could use an LLM
        # to rewrite the response in a specific style.
        styled_response = f"{intro}{response}{outro}"

        return styled_response

    def get_error_response(self) -> str:
        """Returns a personality-appropriate error message."""
        errors = self.current_profile.get('error_messages', ["I'm sorry, I seem to have encountered an error."])
        return random.choice(errors)

if __name__ == '__main__':
    print("--- Testing Enhanced Personality System ---")

    # A sample personality configuration, similar to what would be in settings.yaml
    sample_rules = {
        "default": "professional",
        "profiles": {
            "professional": {
                "greetings": ["Good day. How may I assist you?", "Hello. I am ready to help."],
                "farewells": ["Goodbye.", "I look forward to our next interaction."],
                "response_intros": ["Certainly.", "Based on the information,", "My analysis indicates that"],
                "response_outros": [".", "."],
                "error_messages": ["An error has occurred. Please try again later."]
            },
            "friendly": {
                "greetings": ["Hey there! What's up?", "Hi! What can I do for you today?"],
                "farewells": ["See ya!", "Talk to you later!"],
                "response_intros": ["So, basically,", "Alright, check this out:", "Here's what I think: "],
                "response_outros": ["!", " :)"],
                "error_messages": ["Oops! Something went wrong. My bad!", "Yikes, I hit a snag."]
            }
        }
    }

    # 1. Initialize with default profile
    personality = Personality(sample_rules)
    print(f"\n1. Initialized with default profile: '{personality.current_profile_name}'")
    print(f"  Greeting: {personality.get_greeting()}")

    # 2. Test styling a response
    response_to_style = "the weather seems nice today"
    styled = personality.apply_style(response_to_style)
    print(f"\n2. Styled response (professional): '{styled}'")

    # 3. Switch profile to 'friendly'
    personality.set_profile('friendly')
    print(f"\n3. Switched profile to: '{personality.current_profile_name}'")
    print(f"  New Greeting: {personality.get_greeting()}")

    # 4. Test styling with the new profile
    styled_friendly = personality.apply_style(response_to_style)
    print(f"\n4. Styled response (friendly): '{styled_friendly}'")

    # 5. Test error message
    print(f"\n5. Error message (friendly): '{personality.get_error_response()}'")

    # 6. Switch back to professional
    personality.set_profile('professional')
    print(f"\n6. Switched back to: '{personality.current_profile_name}'")
    print(f"  Error message (professional): '{personality.get_error_response()}'")

    print("\n--- Personality System Test Complete ---")
