# agent/memory.py

import json
import os
import time
from typing import List, Dict, Any

class Memory:
    """
    Manages the agent's memory, including conversation history, learned facts (entities),
    and information about files. It's designed to be more structured and capable
    than a simple list-based memory.
    """

    def __init__(self, paths: Dict[str, str]):
        """
        Initializes the Memory class.

        Args:
            paths (dict): A dictionary containing paths to the memory files.
        """
        self.short_term_path = paths.get('short_term')
        self.long_term_path = paths.get('long_term')

        # Ensure memory store directory exists
        os.makedirs(os.path.dirname(self.short_term_path), exist_ok=True)

        self.short_term_memory: List[Dict[str, str]] = self._load_json(self.short_term_path, default=[])

        # Long-term memory is structured to store entities and their attributes
        self.long_term_memory: Dict[str, Dict[str, Any]] = self._load_json(self.long_term_path, default={"entities": {}, "knowledge": {}})

        # In-session memory for uploaded files (not persisted across restarts)
        self.files: List[Dict[str, str]] = []

    def _load_json(self, file_path: str, default=None):
        """Safely loads a JSON file."""
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return default if default is not None else {}
        return default if default is not None else {}

    def _save_json(self, file_path: str, data: Any):
        """Saves data to a JSON file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def add_to_short_term(self, entry: Dict[str, str]):
        """Adds an entry to the short-term memory (conversation history)."""
        self.short_term_memory.append(entry)
        # We save immediately to ensure state is preserved
        self.save_memory()

    def add_entity_to_long_term(self, entity_name: str, attributes: Dict[str, Any]):
        """
        Adds or updates a structured entity in the long-term memory.
        An entity is a concept, person, place, or thing with associated facts.

        Example:
        add_entity_to_long_term("user_profile", {"name": "Aditya", "preference": "likes dogs"})
        """
        entities = self.long_term_memory.setdefault('entities', {})
        entity = entities.setdefault(entity_name, {})
        entity.update(attributes)
        self.save_memory()

    def add_file_memory(self, filename: str, file_type: str = "unknown", content_summary: str = "N/A"):
        """Adds information about a file to the session's memory."""
        self.files.append({
            "filename": filename,
            "type": file_type,
            "summary": content_summary
        })
        print(f"File '{filename}' added to session memory.")

    def get_conversation_history(self, limit: int = 20) -> List[Dict[str, str]]:
        """Returns the most recent conversation history."""
        return self.short_term_memory[-limit:]

    def get_long_term_entities(self) -> Dict[str, Dict[str, Any]]:
        """Returns all long-term entities."""
        return self.long_term_memory.get('entities', {})

    def add_knowledge(self, source: str, content: str, category: str = "general"):
        """
        Adds a piece of knowledge to the long-term memory's knowledge base.

        Args:
            source (str): The origin of the knowledge (e.g., a filename or URL).
            content (str): The summarized content of the knowledge.
            category (str): A category to classify the knowledge (e.g., 'project_alpha', 'user_preferences').
        """
        knowledge_base = self.long_term_memory.setdefault('knowledge', {})

        # Use a structured format for storing knowledge
        entry_key = f"{category}:{source}"
        knowledge_base[entry_key] = {
            "content": content,
            "source": source,
            "category": category,
            "timestamp": time.time()
        }
        self.save_memory()

    def get_knowledge(self, topic: str, category_filter: str = None) -> List[str]:
        """
        Retrieves knowledge relevant to a topic, with optional category filtering.
        This simulates a more advanced retrieval part of RAG.
        """
        knowledge_base = self.long_term_memory.get('knowledge', {})
        relevant_knowledge = []

        for key, data in knowledge_base.items():
            # Apply category filter if provided
            if category_filter and data.get('category') != category_filter:
                continue

            # Simple keyword search in content, source, and category
            if topic.lower() in data['content'].lower() \
                or topic.lower() in data['source'].lower() \
                or topic.lower() in data['category'].lower():

                relevant_knowledge.append(f"Source: {data['source']} (Category: {data['category']})\nContent: {data['content']}")

        return relevant_knowledge

    def get_file_memory(self) -> List[Dict[str, str]]:
        """Returns information about files in the current session."""
        return self.files

    def clear_short_term_memory(self):
        """Clears the short-term conversation history."""
        self.short_term_memory = []
        self.save_memory()
        print("Short-term memory cleared.")

    def save_memory(self):
        """Saves both short-term and long-term memory to their respective files."""
        self._save_json(self.short_term_path, self.short_term_memory)
        self._save_json(self.long_term_path, self.long_term_memory)

if __name__ == '__main__':
    print("--- Testing Enhanced Memory System ---")

    test_paths = {
        'short_term': 'memory_store/test_short_term.json',
        'long_term': 'memory_store/test_long_term.json'
    }

    # Clean up previous test files
    if os.path.exists(test_paths['short_term']): os.remove(test_paths['short_term'])
    if os.path.exists(test_paths['long_term']): os.remove(test_paths['long_term'])

    # 1. Initialization
    memory = Memory(test_paths)
    print("\n1. Initialized Memory:")
    print(f"  Short-term: {memory.get_conversation_history()}")
    print(f"  Long-term: {memory.get_long_term_entities()}")

    # 2. Add to short-term memory
    memory.add_to_short_term({"role": "user", "content": "My name is Aditya."})
    memory.add_to_short_term({"role": "assistant", "content": "Nice to meet you, Aditya!"})
    print("\n2. After adding to short-term memory:")
    print(f"  Short-term: {memory.get_conversation_history()}")

    # 3. Add a structured entity to long-term memory
    memory.add_entity_to_long_term("user_profile", {"name": "Aditya", "status": "active"})
    memory.add_entity_to_long_term("user_profile", {"interest": "AI agents"})
    print("\n3. After adding entity to long-term memory:")
    print(f"  Long-term Entities: {memory.get_long_term_entities()}")

    # 4. Add file memory
    memory.add_file_memory("project_brief.pdf", file_type="PDF", content_summary="A project about AI.")
    print("\n4. After adding file to session memory:")
    print(f"  File Memory: {memory.get_file_memory()}")

    # 5. Clear short-term memory
    memory.clear_short_term_memory()
    print("\n5. After clearing short-term memory:")
    print(f"  Short-term: {memory.get_conversation_history()}")

    # 6. Verify persistence by reloading
    print("\n6. Verifying persistence...")
    reloaded_memory = Memory(test_paths)
    print(f"  Reloaded Long-term Entities: {reloaded_memory.get_long_term_entities()}")
    print(f"  Reloaded Short-term (should be empty): {reloaded_memory.get_conversation_history()}")

    # Session-only memory should not persist
    print(f"  Reloaded File Memory (should be empty): {reloaded_memory.get_file_memory()}")

    # Clean up test files
    if os.path.exists(test_paths['short_term']): os.remove(test_paths['short_term'])
    if os.path.exists(test_paths['long_term']): os.remove(test_paths['long_term'])

    print("\n--- Memory System Test Complete ---")
