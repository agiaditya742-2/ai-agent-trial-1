import json
import os

class Memory:
    def __init__(self, short_term_file='app/memory_store/short_term.json', long_term_file='app/memory_store/long_term.json'):
        """
        Initializes the Memory class, handling short-term (session) and long-term memory.

        Args:
            short_term_file (str): Path to the JSON file for short-term memory.
            long_term_file (str): Path to the JSON file for long-term memory.
        """
        self.short_term_file = short_term_file
        self.long_term_file = long_term_file
        self._ensure_memory_files_exist()

    def _ensure_memory_files_exist(self):
        """Ensures that the memory storage files exist, creating them if they don't."""
        for file_path in [self.short_term_file, self.long_term_file]:
            dir_name = os.path.dirname(file_path)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump([], f)

    def add_to_short_term(self, entry: str):
        """Adds an entry to the short-term memory."""
        try:
            with open(self.short_term_file, 'r+') as f:
                memory = json.load(f)
                memory.append(entry)
                f.seek(0)
                json.dump(memory, f, indent=4)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error accessing short-term memory: {e}")

    def get_history(self) -> list:
        """Retrieves the entire conversation history from short-term memory."""
        try:
            with open(self.short_term_file, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            return []

    def clear_short_term(self):
        """Clears the short-term memory."""
        with open(self.short_term_file, 'w') as f:
            json.dump([], f)
