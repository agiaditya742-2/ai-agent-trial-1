import yaml
import os

class Personality:
    def __init__(self, config_file='app/config/settings.yaml'):
        """
        Initializes the Personality class by loading agent settings.

        Args:
            config_file (str): Path to the YAML configuration file.
        """
        # Ensure the path is correct relative to the project root
        self._load_config(config_file)

    def _load_config(self, config_file):
        """Loads the personality configuration from a YAML file."""
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file not found at: {config_file}")

        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
            self.settings = config.get('personality', {})

    def get_name(self) -> str:
        """Returns the agent's name."""
        return self.settings.get('name', 'AI Agent')

    def get_role(self) -> str:
        """Returns the agent's role."""
        return self.settings.get('role', 'Assistant')

    def get_rules(self) -> list:
        """Returns the agent's behavioral rules."""
        return self.settings.get('rules', [])
