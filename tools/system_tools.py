# tools/system_tools.py

import datetime

class SystemTools:
    """
    A collection of tools for safe interaction with the local system.

    This class provides methods for accessing system information, like the
    current time or date. These are designed to be safe operations that do not
    modify the system state (e.g., no file writing or command execution).
    """

    def get_current_time(self):
        """
        Retrieves the current local time.

        Returns:
            str: A string representing the current time.
        """
        print("[SystemTools] Getting current time...")
        now = datetime.datetime.now()
        return f"The current time is {now.strftime('%I:%M:%S %p')}."

    def get_current_date(self):
        """
        Retrieves the current local date.

        Returns:
            str: A string representing the current date.
        """
        print("[SystemTools] Getting current date...")
        today = datetime.date.today()
        return f"Today's date is {today.strftime('%B %d, %Y')}."

if __name__ == '__main__':
    # Example usage for testing the SystemTools directly

    system_tools = SystemTools()

    # Test case 1: Get the current time
    current_time = system_tools.get_current_time()
    print(f"Time request:\n{current_time}\n")

    # Test case 2: Get the current date
    current_date = system_tools.get_current_date()
    print(f"Date request:\n{current_date}\n")
