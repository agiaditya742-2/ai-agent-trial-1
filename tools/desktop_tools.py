# tools/desktop_tools.py

"""
Provides a set of simulated tools for interacting with a desktop environment.

This module is designed for demonstration purposes and does not perform real
file system or application-level operations. Instead, it logs the actions that
it *would* take, providing a safe way to illustrate the agent's capabilities
without posing a security risk.
"""

import logging
import os
import time

# Configure logging for this module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - (DesktopTools) - %(message)s')

class DesktopTools:
    """A collection of simulated tools for desktop automation."""

    def __init__(self):
        # We can maintain a simulated state for more complex interactions
        self.simulated_clipboard = ""
        self.simulated_open_apps = set()
        # Simulate a basic file system structure for realism
        self.simulated_fs = {
            "Documents": ["project_plan.txt", "meeting_notes.docx"],
            "Downloads": ["installer.exe", "image.jpg"],
            "Desktop": ["shortcut.lnk"]
        }

    def open_application(self, app_name: str) -> str:
        """
        Simulates opening a desktop application.

        Args:
            app_name (str): The name of the application to open (e.g., "VS Code", "Chrome").

        Returns:
            str: A confirmation message.
        """
        logging.info(f"SIMULATING: Opening application '{app_name}'.")
        if app_name in self.simulated_open_apps:
            return f"Application '{app_name}' is already running."
        self.simulated_open_apps.add(app_name)
        return f"Successfully opened application: {app_name}."

    def close_application(self, app_name: str) -> str:
        """
        Simulates closing a desktop application.

        Args:
            app_name (str): The name of the application to close.

        Returns:
            str: A confirmation message.
        """
        logging.info(f"SIMULATING: Closing application '{app_name}'.")
        if app_name in self.simulated_open_apps:
            self.simulated_open_apps.remove(app_name)
            return f"Application '{app_name}' has been closed."
        return f"Application '{app_name}' is not currently running."

    def list_files(self, directory: str) -> str:
        """
        Simulates listing files in a directory.

        Args:
            directory (str): The name of the directory to list (e.g., "Documents").

        Returns:
            str: A string containing the list of files, or an error message.
        """
        logging.info(f"SIMULATING: Listing files in directory '{directory}'.")
        if directory in self.simulated_fs:
            files = self.simulated_fs[directory]
            if not files:
                return f"Directory '{directory}' is empty."
            file_list_str = "\n".join(f"- {file}" for file in files)
            return f"Files in '{directory}':\n{file_list_str}"
        return f"Error: Directory '{directory}' not found."

    def create_file(self, filename: str, content: str = "") -> str:
        """
        Simulates creating a new file with optional content.

        Args:
            filename (str): The name of the file to create (e.g., "notes.txt").
            content (str, optional): The content to write to the file. Defaults to "".

        Returns:
            str: A confirmation message.
        """
        logging.info(f"SIMULATING: Creating file '{filename}' with content.")
        # For simulation, we'll just place it on the "Desktop"
        if "Desktop" in self.simulated_fs:
            self.simulated_fs["Desktop"].append(filename)
            # We could also simulate saving the content if needed
            return f"Successfully created file '{filename}' on the Desktop."
        return "Error: Could not find Desktop to create file."

    def set_clipboard(self, text: str) -> str:
        """
        Simulates setting the system clipboard text.

        Args:
            text (str): The text to place in the clipboard.

        Returns:
            str: A confirmation message.
        """
        logging.info("SIMULATING: Setting clipboard text.")
        self.simulated_clipboard = text
        return "Clipboard has been set."

    def get_clipboard(self) -> str:
        """
        Simulates getting the current text from the system clipboard.

        Returns:
            str: The text from the clipboard.
        """
        logging.info("SIMULATING: Getting clipboard text.")
        if not self.simulated_clipboard:
            return "The clipboard is currently empty."
        return f"Clipboard content: '{self.simulated_clipboard}'"

if __name__ == '__main__':
    print("--- Testing Simulated Desktop Tools ---")
    tools = DesktopTools()

    # Test Application Management
    print("\n[1] Application Management")
    print(f"Action: Open Chrome -> {tools.open_application('Chrome')}")
    print(f"Action: Open Chrome again -> {tools.open_application('Chrome')}")
    print(f"Action: Close Chrome -> {tools.close_application('Chrome')}")
    print(f"Action: Close Chrome again -> {tools.close_application('Chrome')}")

    # Test File System
    print("\n[2] File System")
    print(f"Action: List Documents -> \n{tools.list_files('Documents')}")
    print(f"Action: Create a file -> {tools.create_file('my_new_file.txt', 'This is a test.')}")
    print(f"Action: List Desktop -> \n{tools.list_files('Desktop')}")
    print(f"Action: List Downloads -> \n{tools.list_files('Downloads')}")

    # Test Clipboard
    print("\n[3] Clipboard")
    print(f"Action: Get Clipboard -> {tools.get_clipboard()}")
    print(f"Action: Set Clipboard -> {tools.set_clipboard('Hello from the AI agent!')}")
    print(f"Action: Get Clipboard again -> {tools.get_clipboard()}")

    print("\n--- Desktop Tools Test Complete ---")
