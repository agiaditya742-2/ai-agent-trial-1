# main.py

from agent.core_agent import CoreAgent

def main():
    """
    The main entry point for the AI Agent application.

    This function initializes the CoreAgent and starts its main loop,
    allowing the user to interact with the agent.
    """
    print("Initializing AI Agent...")

    # Create an instance of the CoreAgent.
    # The CoreAgent will load its configuration and all sub-components.
    try:
        agent = CoreAgent(config_path='config/settings.yaml')
    except Exception as e:
        print(f"Failed to initialize the CoreAgent. Error: {e}")
        return

    # Start the agent's interactive loop.
    # The agent will now wait for user input.
    try:
        agent.start()
    except KeyboardInterrupt:
        print("\nUser interrupted the session.")
        agent.stop()
    except Exception as e:
        print(f"An unexpected error occurred during agent execution: {e}")
        agent.stop()

if __name__ == '__main__':
    # This ensures the main() function is called only when the script is executed directly.
    main()
