# agents/task_agent.py

import json
import os

class TaskAgent:
    """
    Manages task planning, decomposition, and execution.

    This agent is responsible for handling tasks that may require multiple steps
    or need to be remembered over time, like reminders or to-do list items.

    This version saves tasks to a JSON file to make them persistent across
    sessions.
    """

    def __init__(self, tasks_file='memory_store/tasks.json'):
        """
        Initializes the TaskAgent and loads tasks from a file.

        Args:
            tasks_file (str): The path to the JSON file for storing tasks.
        """
        self.tasks_file = tasks_file
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        """
        Loads tasks from the JSON file.

        Returns:
            list: The list of tasks, or an empty list if the file is not found.
        """
        if not os.path.exists(self.tasks_file):
            return []
        try:
            with open(self.tasks_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_tasks(self):
        """
        Saves the current list of tasks to the JSON file.
        """
        os.makedirs(os.path.dirname(self.tasks_file), exist_ok=True)
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=4)

    def execute(self, user_input):
        """
        Parses the user input to determine the desired task operation.

        Args:
            user_input (str): The user's command related to a task.

        Returns:
            str: A confirmation or the result of the task operation.
        """
        print(f"[TaskAgent] Processing input: '{user_input}'")

        # Simplified logic to differentiate between adding and listing tasks
        if user_input.lower().startswith("remind me to") or user_input.lower().startswith("add task"):
            return self._add_task(user_input)
        elif "what are my tasks" in user_input.lower() or "list tasks" in user_input.lower():
            return self._list_tasks()
        else:
            return "I'm not sure how to handle that task. Try 'add task' or 'list tasks'."

    def _add_task(self, task_description):
        """
        Adds a new task to the task list.

        Args:
            task_description (str): The full user command for adding a task.

        Returns:
            str: A confirmation message.
        """
        # A simple way to extract the task from the command
        task = task_description.replace("remind me to", "").replace("add task", "").strip()

        if task:
            self.tasks.append(task)
            self._save_tasks()  # Save tasks after adding a new one
            print(f"[TaskAgent] Added task: '{task}'")
            return f"Okay, I've added '{task}' to your to-do list."
        else:
            return "What task would you like to add?"

    def _list_tasks(self):
        """
        Lists all the current tasks.

        Returns:
            str: A string containing the list of tasks, or a message if empty.
        """
        print("[TaskAgent] Listing tasks.")
        if not self.tasks:
            return "You have no tasks in your to-do list."
        else:
            # Format the list for display
            task_list_str = "\n".join(f"- {task}" for task in self.tasks)
            return f"Here are your current tasks:\n{task_list_str}"

if __name__ == '__main__':
    # Example usage for testing the TaskAgent directly

    task_agent = TaskAgent()

    # Test case 1: Add a task
    add_command_1 = "remind me to buy milk"
    add_response_1 = task_agent.execute(add_command_1)
    print(f"User: '{add_command_1}'\nAgent: '{add_response_1}'\n")

    # Test case 2: Add another task
    add_command_2 = "add task finish the project report"
    add_response_2 = task_agent.execute(add_command_2)
    print(f"User: '{add_command_2}'\nAgent: '{add_response_2}'\n")

    # Test case 3: List the tasks
    list_command = "what are my tasks"
    list_response = task_agent.execute(list_command)
    print(f"User: '{list_command}'\nAgent: '{list_response}'\n")

    # Test case 4: Handle an unknown command
    unknown_command = "are my tasks done?"
    unknown_response = task_agent.execute(unknown_command)
    print(f"User: '{unknown_command}'\nAgent: '{unknown_response}'\n")
