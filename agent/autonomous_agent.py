# agent/autonomous_agent.py

import time
import logging
from threading import Event
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - (AutonomousAgent) - %(message)s')

class AutonomousAgent:
    """
    An agent capable of autonomous operation to achieve a specific goal.
    It creates a plan, executes it step-by-step, and can even attempt to
    self-correct if it fails. It operates in a separate thread.
    """

    def __init__(self, goal: str, core_agent):
        self.goal: str = goal
        self.core_agent = core_agent  # Direct access to the core agent's tools
        self.plan: List[str] = []
        self.task_log: List[Dict[str, Any]] = []
        self.is_running: bool = False
        self.stop_event = Event()

    def run(self):
        """The main entry point for the agent's execution thread."""
        self.is_running = True
        self._log_entry("Start", f"Autonomous agent activated. Goal: {self.goal}")

        try:
            self._create_plan()

            for i, step in enumerate(self.plan):
                if self.stop_event.is_set():
                    self._log_entry("Halted", "Agent was stopped by user command.")
                    break

                self._execute_step(i + 1, step)
            else: # This 'else' belongs to the 'for' loop, executing only if the loop completes without a break
                self._log_entry("Finish", "Autonomous agent has completed its plan.")

        except Exception as e:
            logging.error(f"A critical error occurred in the autonomous agent: {e}")
            self._log_entry("Critical Failure", f"Agent stopped due to an unexpected error: {e}", "error")

        finally:
            self.is_running = False

    def _create_plan(self):
        """
        Creates a multi-step plan to achieve the goal using an LLM.
        """
        self._log_entry("Planning", "Formulating a plan to achieve the goal.")

        # In a real system, this prompt would be much more complex.
        # For simulation, we create a plan based on keywords.
        if "research" in self.goal.lower():
            topic = self.goal.lower().replace("research", "").strip()
            self.plan = [
                f"search for benefits of {topic}",
                f"read website from the first result",
                f"summarize findings about {topic}"
            ]
        elif "organize project" in self.goal.lower():
            self.plan = [
                "list files in Documents",
                "create file 'project_summary.txt' with content 'This is a summary of the new project.'",
                "add task 'review project_summary.txt'"
            ]
        else:
            self.plan = [f"search for '{self.goal}'"]

        self._log_entry("Plan Created", f"Plan formulated with {len(self.plan)} steps.", "success")

    def _execute_step(self, step_num: int, step_description: str):
        """
        Executes a single step from the plan and attempts to self-correct on failure.
        """
        self._log_entry(f"Step {step_num}", f"Executing: {step_description}")

        max_retries = 2
        for i in range(max_retries):
            try:
                # Use the CoreAgent's tool agent to execute the action
                tool_agent = self.core_agent.agent_manager.get_agent('tool_agent')
                if not tool_agent:
                    raise RuntimeError("ToolAgent not available.")

                result = tool_agent.execute(step_description)

                if result.get("status") in ["error", "failed"]:
                    raise RuntimeError(result.get("result"))

                self._log_entry(f"Step {step_num} Result", str(result), "success")
                time.sleep(2) # Simulate work
                return # Step was successful

            except Exception as e:
                logging.warning(f"Step {step_num} failed on attempt {i + 1}/{max_retries}. Error: {e}")
                self._log_entry(f"Step {step_num} Failure", f"Attempt {i + 1} failed: {e}", "warning")

                if i < max_retries - 1:
                    self._self_correct(step_description, str(e))
                else:
                    self._log_entry(f"Step {step_num} Failure", "Maximum retries reached. Aborting plan.", "error")
                    self.stop() # Abort the entire plan

    def _self_correct(self, failed_step: str, error_message: str):
        """
        Simulates an LLM-based self-correction step.
        """
        self._log_entry("Self-Correction", f"Attempting to correct for error: {error_message}")
        time.sleep(1) # Simulate thinking
        # In a real system, this would involve another LLM call to create a new plan or modify the step.
        # For simulation, we'll just log that we tried.
        self._log_entry("Self-Correction", "Formulated a corrective action (simulated).", "info")

    def stop(self):
        """Stops the agent's execution."""
        if self.is_running:
            logging.info("Stopping autonomous agent...")
            self.stop_event.set()

    def get_status(self) -> Dict[str, Any]:
        """Returns the current status and log of the agent."""
        return {
            "goal": self.goal,
            "is_running": self.is_running,
            "plan": self.plan,
            "task_log": self.task_log
        }

    def _log_entry(self, step: str, details: str, level: str = "info"):
        """Adds a structured entry to the task log."""
        log_item = {"step": step, "details": details, "timestamp": time.time(), "level": level}
        self.task_log.append(log_item)
        logging.info(f"({step}) - {details}")
