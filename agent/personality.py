# agent/personality.py

import random
import time
from typing import Dict, Any, List

class Personality:
    """
    Manages the agent's personality, including its communication style,
    dynamic moods, and complex response construction. This class is designed
    to make the agent feel more lifelike and engaging.
    """

    def __init__(self, personality_rules: Dict[str, Any]):
        """
        Initializes the Personality class.

        Args:
            personality_rules (dict): A config dict with profiles, moods, etc.
        """
        self.profiles: Dict[str, Any] = personality_rules.get('profiles', {})
        self.default_profile: str = personality_rules.get('default', 'neutral')
        self.current_profile_name: str = self.default_profile
        self.current_profile: Dict[str, Any] = self.profiles.get(self.current_profile_name, {})

        # Mood dynamics
        self.moods: Dict[str, Any] = personality_rules.get('moods', {})
        self.current_mood: str = self.current_profile.get('default_mood', 'neutral')
        self.mood_intensity: float = 0.5  # Range from 0.0 to 1.0

    def set_profile(self, profile_name: str) -> bool:
        """
        Sets the agent's active personality profile.
        """
        if profile_name in self.profiles:
            self.current_profile_name = profile_name
            self.current_profile = self.profiles[profile_name]
            self.current_mood = self.current_profile.get('default_mood', 'neutral')
            print(f"Personality profile set to '{profile_name}'.")
            return True
        print(f"Warning: Personality profile '{profile_name}' not found.")
        return False

    def update_mood(self, conversation_history: List[Dict[str, str]]):
        """
        Updates the agent's mood based on the recent conversation.
        This is a simplified simulation of sentiment analysis.
        """
        last_user_message = ""
        if conversation_history and conversation_history[-1]['role'] == 'user':
            last_user_message = conversation_history[-1]['content'].lower()

        # Simple keyword-based mood shifting
        positive_words = ['thanks', 'great', 'awesome', 'cool', 'love it']
        negative_words = ['wrong', 'stupid', 'hate', 'bad', 'useless']

        if any(word in last_user_message for word in positive_words):
            self.mood_intensity = min(1.0, self.mood_intensity + 0.2)
            self.current_mood = self.current_profile.get('positive_mood', 'happy')
            print(f"Mood shifted towards {self.current_mood} (Intensity: {self.mood_intensity:.2f})")
        elif any(word in last_user_message for word in negative_words):
            self.mood_intensity = max(0.0, self.mood_intensity - 0.2)
            self.current_mood = self.current_profile.get('negative_mood', 'annoyed')
            print(f"Mood shifted towards {self.current_mood} (Intensity: {self.mood_intensity:.2f})")

    def get_greeting(self) -> str:
        """Returns a greeting based on current profile and mood."""
        return self._get_dynamic_response('greetings')

    def get_farewell(self) -> str:
        """Returns a farewell based on current profile and mood."""
        return self._get_dynamic_response('farewells')

    def apply_style(self, response: str) -> str:
        """
        Applies the current personality's style to a given response,
        taking mood into account.
        """
        intro = self._get_dynamic_response('response_intros')
        outro = self._get_dynamic_response('response_outros')

        # A more advanced version could use an LLM to rewrite the response
        return f"{intro} {response} {outro}".strip()

    def get_error_response(self) -> str:
        """Returns a personality-appropriate error message."""
        return self._get_dynamic_response('error_messages')

    def _get_dynamic_response(self, response_type: str) -> str:
        """
        Selects a response from the profile, considering the current mood.
        It falls back from mood-specific to general to default phrases.
        """
        # 1. Try to get a mood-specific response list
        mood_specific_key = f"{self.current_mood}_{response_type}"
        response_list = self.current_profile.get(mood_specific_key)

        # 2. If not found, try the general response list for the type
        if not response_list:
            response_list = self.current_profile.get(response_type)

        # 3. If still not found, use a fallback
        if not response_list:
            return ""

        return random.choice(response_list)

if __name__ == '__main__':
    # Sample config to demonstrate the new features
    sample_config = {
        "default": "assistant",
        "profiles": {
            "assistant": {
                "default_mood": "neutral",
                "positive_mood": "pleased",
                "negative_mood": "concerned",
                "greetings": ["Hello. How can I assist?"],
                "pleased_greetings": ["It's a pleasure to be of service today!", "Hello! I'm happy to help."],
                "response_intros": ["Certainly,", "The answer is"],
                "pleased_response_intros": ["Absolutely!", "I'd be delighted to explain."],
                "concerned_response_intros": ["I understand your concern.", "I need to point out that"],
                "response_outros": ["."],
                "error_messages": ["An error has occurred."]
            }
        }
    }

    p = Personality(sample_config)
    print("--- Testing Enhanced Personality with Moods ---")

    # 1. Default state
    print(f"\n[1] Default Greeting: {p.get_greeting()}")
    print(f"Styled Response: {p.apply_style('the data is correct')}")

    # 2. Positive interaction
    positive_history = [{"role": "user", "content": "that's great, thanks!"}]
    p.update_mood(positive_history)
    print(f"\n[2] Mood after positive feedback: {p.current_mood}")
    print(f"Greeting (Pleased): {p.get_greeting()}")
    print(f"Styled Response (Pleased): {p.apply_style('the data is correct')}")

    # 3. Negative interaction
    negative_history = [{"role": "user", "content": "that's a stupid answer"}]
    p.update_mood(negative_history)
    print(f"\n[3] Mood after negative feedback: {p.current_mood}")
    print(f"Styled Response (Concerned): {p.apply_style('the data is correct')}")

    print("\n--- Personality Test Complete ---")
