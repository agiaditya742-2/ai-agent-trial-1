# agent/memory.py

import json
import os

class Memory:
    """
    Manages the agent's short-term and long-term memory.

    This class is responsible for loading, saving, and providing access to the
    agent's memory stores. Short-term memory holds the context of the current
    conversation, while long-term memory stores important information that
    needs to be retained across sessions.
    """

    def __init__(self, paths):
        """
        Initializes the Memory class and loads existing memory from files.

        Args:
            paths (dict): A dictionary containing paths to the memory files.
                          Example: {'short_term': 'path/to/short.json', 'long_term': 'path/to/long.json'}
        """
        self.short_term_path = paths.get('short_term')
        self.long_term_path = paths.get('long_term')

        self.short_term_memory = self._load_json(self.short_term_path)
        self.long_term_memory = self._load_json(self.long_term_path)

    def _load_json(self, path):
        """
        Safely loads a JSON file.

        Args:
            path (str): The path to the JSON file.

        Returns:
            list: The loaded data, or an empty list if the file does not exist or is invalid.
        """
        if not path or not os.path.exists(path):
            return []
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_json(self, path, data):
        """
        Saves data to a JSON file.

        Args:
            path (str): The path to the JSON file.
            data (list): The data to be saved.
        """
        if not path:
            return
        # Ensure the directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

    def add_to_short_term(self, data):
        """
        Adds an entry to the short-term memory.

        Args:
            data (dict): The data to be added (e.g., a message).
        """
        self.short_term_memory.append(data)

    def get_short_term_memory(self):
        """
        Retrieves the entire short-term memory.

        Returns:
            list: The short-term memory.
        """
        return self.short_term_memory

    def get_long_term_memory(self):
        """
        Retrieves the entire long-term memory.

        Returns:
            list: The long-term memory.
        """
        return self.long_term_memory

    def add_to_long_term(self, data):
        """
        Adds an entry to the long-term memory.

        Args:
            data (dict): The data to be added (e.g., a key fact or summary).
        """
        self.long_term_memory.append(data)

    def clear_short_term_memory(self):
        """
        Clears the short-term memory and the corresponding file.
        """
        self.short_term_memory = []
        # Overwrite the file with an empty list
        self._save_json(self.short_term_path, [])
        print("Short-term memory cleared.")

    def get_conversation_history(self, num_messages=10):
        """
        Retrieves the most recent messages from short-term memory.

        Args:
            num_messages (int): The number of recent messages to retrieve.

        Returns:
            list: A list of the most recent messages.
        """
        return self.short_term_memory[-num_messages:]

    def consolidate_memory(self):
        """
        Moves information from short-term to long-term memory.

        This is a placeholder for a more complex summarization and consolidation
        logic. In this simple implementation, it moves the entire short-term
        history to long-term and clears short-term memory.
        """
        print("Consolidating memory...")
        self.long_term_memory.extend(self.short_term_memory)
        self.short_term_memory = []
        print("Memory consolidated.")

    def save_memory(self):
        """
        Saves both short-term and long-term memory to their respective files.
        """
        print("Saving memory...")
        self._save_json(self.short_term_path, self.short_term_memory)
        self._save_json(self.long_term_path, self.long_term_memory)
        print("Memory saved.")

if __name__ == '__main__':
    # Example usage for testing the Memory class

    # Define paths for dummy memory files
    test_paths = {
        'short_term': 'memory_store/short_term_test.json',
        'long_term': 'memory_store/long_term_test.json'
    }

    # Ensure the test files are clean before starting
    if os.path.exists(test_paths['short_term']):
        os.remove(test_paths['short_term'])
    if os.path.exists(test_paths['long_term']):
        os.remove(test_paths['long_term'])

    # 1. Initialize Memory
    memory = Memory(test_paths)
    print(f"Initial short-term memory: {memory.get_short_term_memory()}")
    print(f"Initial long-term memory: {memory.get_long_term_memory()}")

    # 2. Add some data to short-term memory
    memory.add_to_short_term({"role": "user", "content": "Hello, agent!"})
    memory.add_to_short_term({"role": "assistant", "content": "Hello, user!"})
    print(f"Updated short-term memory: {memory.get_short_term_memory()}")

    # 3. Consolidate memory
    memory.consolidate_memory()
    print(f"Short-term after consolidation: {memory.get_short_term_memory()}")
    print(f"Long-term after consolidation: {memory.get_long_term_memory()}")

    # 4. Add new data to short-term memory
    memory.add_to_short_term({"role": "user", "content": "How are you?"})
    print(f"New short-term memory: {memory.get_short_term_memory()}")

    # 5. Save all memory to files
    memory.save_memory()

    # 6. Verify by creating a new Memory instance and loading the data
    print("\n--- Verifying persistence ---")
    new_memory = Memory(test_paths)
    print(f"Loaded short-term memory: {new_memory.get_short_term_memory()}")
    print(f"Loaded long-term memory: {new_memory.get_long_term_memory()}")

    # Clean up test files
    os.remove(test_paths['short_term'])
    os.remove(test_paths['long_term'])
