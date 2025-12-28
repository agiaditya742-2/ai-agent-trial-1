# agent/autonomous_agent.py

"""
The Autonomous Agent component.

This agent is designed to execute long-running tasks by creating a plan,
using tools to execute the plan, and managing its own state. It's the key
to enabling the AI to work by itself on complex goals.
"""

import time
import logging
from threading import Thread, Event
from typing import Dict, Any, List

# A simulated toolset for the autonomous agent
from tools.internet_tools import search_web, read_website_content

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AutonomousAgent:
    """
    An agent capable of autonomous operation to achieve a specific goal.

    This agent operates in a separate thread, allowing it to run in the background
    without blocking the main application (e.g., the web server).
    """

    def __init__(self, goal: str):
        self.goal: str = goal
        self.plan: List[str] = []
        self.task_log: List[Dict[str, Any]] = []
        self.is_running: bool = False
        self.stop_event = Event()
        self.thread: Thread = None

    def _create_plan(self):
        """
        Simulates the creation of a multi-step plan to achieve the goal.

        In a real LLM-powered agent, this would involve a complex prompt to a language model
        asking it to decompose the goal into a series of actionable steps.
        """
        logging.info(f"Creating a plan for goal: '{self.goal}'")
        # Simulate a plan based on a generic research goal
        self.plan = [
            f"search_web: 'what is {self.goal}'",
            "read_website_content: from first search result",
            f"search_web: 'how to implement {self.goal}'",
            "read_website_content: from second search result",
            "synthesize_findings: 'create a summary of the key findings'"
        ]
        self.task_log.append({"step": "Plan Creation", "details": f"Plan created with {len(self.plan)} steps."})

    def _execute_step(self, step: str):
        """
        Executes a single step from the plan.

        This method parses the step to determine which tool to use and with what arguments.
        It's a simplified simulation of a tool-calling architecture.
        """
        if self.stop_event.is_set():
            logging.info("Stop event received, halting execution.")
            return

        logging.info(f"Executing step: {step}")
        parts = step.split(": ", 1)
        tool_name = parts[0]
        args = parts[1] if len(parts) > 1 else ""

        result = "No result."
        try:
            if tool_name == "search_web":
                result = search_web(args)
            elif tool_name == "read_website_content":
                # For this simulation, we'll just grab a URL from the previous step's log
                previous_search_results = self.task_log[-1].get("result", "{}")
                import json
                try:
                    urls = [res['url'] for res in json.loads(previous_search_results).get('results', [])]
                    if urls:
                        result = read_website_content(urls[0])
                    else:
                        result = "Could not find a URL from the previous step."
                except (json.JSONDecodeError, IndexError):
                    result = "Error processing previous search results to find a URL."
            elif tool_name == "synthesize_findings":
                # This is a high-level task that would typically involve another LLM call
                result = f"Simulated synthesis: Based on the research, the key findings about '{self.goal}' have been compiled into a summary."
            else:
                result = f"Unknown tool: {tool_name}"

            self.task_log.append({"step": step, "result": result, "status": "Completed"})
            time.sleep(2)  # Simulate time taken for the task
        except Exception as e:
            logging.error(f"Error executing step '{step}': {e}")
            self.task_log.append({"step": step, "error": str(e), "status": "Failed"})

    def _run_loop(self):
        """The main loop for the agent's execution thread."""
        self.is_running = True
        self.task_log.append({"step": "Start", "details": f"Autonomous agent started for goal: {self.goal}"})

        self._create_plan()

        for step in self.plan:
            if self.stop_event.is_set():
                break
            self._execute_step(step)

        self.is_running = False
        self.task_log.append({"step": "Finish", "details": "Autonomous agent has completed its goal."})
        logging.info(f"Autonomous agent for goal '{self.goal}' has finished.")

    def start(self):
        """Starts the autonomous agent in a new thread."""
        if not self.is_running:
            logging.info("Starting autonomous agent...")
            self.stop_event.clear()
            self.thread = Thread(target=self._run_loop)
            self.thread.start()

    def stop(self):
        """Stops the agent's execution."""
        if self.is_running:
            logging.info("Stopping autonomous agent...")
            self.stop_event.set()
            if self.thread:
                self.thread.join()  # Wait for the thread to finish
            self.is_running = False

    def get_status(self):
        """Returns the current status and log of the agent."""
        return {
            "goal": self.goal,
            "is_running": self.is_running,
            "plan": self.plan,
            "task_log": self.task_log
        }

if __name__ == '__main__':
    print("--- Testing Autonomous Agent ---")

    # Define a goal for the agent
    agent_goal = "Quantum Computing"
    autonomous_agent = AutonomousAgent(goal=agent_goal)

    # Start the agent
    autonomous_agent.start()

    # Monitor its progress for a few seconds
    for i in range(10):
        if not autonomous_agent.is_running:
            break
        status = autonomous_agent.get_status()
        print(f"\n--- Status Update (Second {i+1}) ---")
        print(f"Is Running: {status['is_running']}")
        print("Task Log:")
        for log in status['task_log']:
            print(f"  - {log}")
        time.sleep(1)

    # Stop the agent if it's still running
    if autonomous_agent.is_running:
        autonomous_agent.stop()

    print("\n--- Final Status ---")
    final_status = autonomous_agent.get_status()
    import json
    print(json.dumps(final_status, indent=2))

    print("\n--- Autonomous Agent Test Complete ---")
