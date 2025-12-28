# agents/task_agent.py

import json
import os
import logging
from typing import List, Dict, Any

# Configure logging for this module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - (TaskAgent) - %(message)s')

class TaskAgent:
    """
    Manages complex tasks, including to-do lists, reminders, and multi-step plans.
    Tasks are persistent and saved to a JSON file.
    """

    def __init__(self, tasks_file='memory_store/tasks.json'):
        """
        Initializes the TaskAgent and loads tasks from a file.
        """
        self.tasks_file = tasks_file
        self.tasks: List[Dict[str, Any]] = self._load_tasks()

    def _load_tasks(self) -> List[Dict[str, Any]]:
        """
        Loads tasks from the JSON file. If the file doesn't exist, returns an empty list.
        """
        if not os.path.exists(self.tasks_file):
            return []
        try:
            with open(self.tasks_file, 'r') as f:
                tasks = json.load(f)
                # Ensure tasks are in the new format
                return [t if isinstance(t, dict) else {"description": t, "completed": False} for t in tasks]
        except (json.JSONDecodeError, FileNotFoundError):
            logging.warning("Could not load or parse tasks file. Starting with an empty list.")
            return []

    def _save_tasks(self):
        """
        Saves the current list of tasks to the JSON file.
        """
        try:
            os.makedirs(os.path.dirname(self.tasks_file), exist_ok=True)
            with open(self.tasks_file, 'w') as f:
                json.dump(self.tasks, f, indent=4)
        except IOError as e:
            logging.error(f"Could not save tasks to file '{self.tasks_file}'. Error: {e}")

    def execute(self, user_input: str) -> str:
        """
        Parses the user's command and routes to the appropriate task function.
        """
        user_input = user_input.lower()
        logging.info(f"Processing task command: '{user_input}'")

        # Routing logic for task operations
        if user_input.startswith("add task") or user_input.startswith("remind me to"):
            return self._add_task(user_input)
        elif "list tasks" in user_input or "what are my tasks" in user_input:
            return self._list_tasks()
        elif user_input.startswith("complete task") or user_input.startswith("finish task"):
            return self._complete_task(user_input)
        elif "clear all tasks" in user_input:
            return self._clear_tasks()
        else:
            return "I'm not sure how to handle that task. Try 'add', 'list', or 'complete'."

    def _add_task(self, command: str) -> str:
        """Adds a new task."""
        description = command.replace("add task", "").replace("remind me to", "").strip()
        if not description:
            return "What is the task you would like to add?"

        new_task = {"description": description, "completed": False}
        self.tasks.append(new_task)
        self._save_tasks()
        logging.info(f"Added new task: '{description}'")
        return f"Task added: '{description}'."

    def _list_tasks(self) -> str:
        """Lists all current tasks, showing their status."""
        if not self.tasks:
            return "Your task list is empty."

        response = "Here are your tasks:\n"
        for i, task in enumerate(self.tasks):
            status = "✓" if task.get('completed') else " "
            response += f"{i + 1}. [{status}] {task['description']}\n"
        return response.strip()

    def _complete_task(self, command: str) -> str:
        """Marks a task as complete by its number."""
        try:
            # Extract the number from "complete task 1"
            task_num_str = command.split()[-1]
            task_index = int(task_num_str) - 1

            if 0 <= task_index < len(self.tasks):
                if self.tasks[task_index]['completed']:
                    return f"Task {task_num_str} was already marked as complete."

                self.tasks[task_index]['completed'] = True
                self._save_tasks()
                logging.info(f"Completed task {task_num_str}: '{self.tasks[task_index]['description']}'")
                return f"Great! I've marked task {task_num_str} as complete."
            else:
                return "That task number is not on your list."
        except (ValueError, IndexError):
            return "Please specify a valid task number to complete (e.g., 'complete task 1')."

    def _clear_tasks(self) -> str:
        """Clears all tasks from the list."""
        self.tasks = []
        self._save_tasks()
        logging.info("All tasks have been cleared.")
        return "Your task list has been cleared."

if __name__ == '__main__':
    print("--- Testing Expanded TaskAgent ---")
    agent = TaskAgent('memory_store/test_tasks.json')
    agent._clear_tasks() # Ensure a clean state

    # 1. Add tasks
    print(agent.execute("add task Buy groceries"))
    print(agent.execute("remind me to Call the doctor"))

    # 2. List tasks
    print("\n[2] Listing tasks:")
    print(agent.execute("list tasks"))

    # 3. Complete a task
    print("\n[3] Completing a task:")
    print(agent.execute("complete task 1"))
    print(agent.execute("list tasks"))

    # 4. Clear tasks
    print("\n[4] Clearing tasks:")
    print(agent.execute("clear all tasks"))
    print(agent.execute("list tasks"))

    if os.path.exists('memory_store/test_tasks.json'):
        os.remove('memory_store/test_tasks.json')

    print("\n--- TaskAgent Test Complete ---")
