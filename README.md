# trial-ai-agent-1: A Modular AI Agent System

Welcome to **trial-ai-agent-1**, a production-grade, extensible AI Agent system designed for daily assistance, automation, learning, and task execution. This project serves as a comprehensive portfolio piece for software engineers, AI engineers, and ML engineers looking to demonstrate their skills in building complex, real-world AI systems.

![AI Agent Banner](https://i.imgur.com/your-banner-image.png) <!-- Placeholder for a banner image -->

---

## 1. Project Description

This project implements a modular, multi-component AI agent platform, moving beyond a simple chatbot to a sophisticated system capable of multi-agent coordination, task decomposition, and tool usage. The agent is designed to be extensible, allowing for the easy addition of new capabilities, AI models, and tools. It operates via a command-line interface (CLI) and supports both text-based and voice-based interactions (in a simulated capacity).

## 2. Key Features

- **Modular Architecture:** The system is broken down into distinct components (core agent, sub-agents, tools, memory), promoting separation of concerns and maintainability.
- **Multi-Agent System:** Features specialized agents for different tasks (chat, voice, tools, tasks), coordinated by a central `CoreAgent`.
- **Tool & API Integration:** Built with a tool-calling architecture, allowing the agent to use external and internal tools to perform actions.
- **Config-Driven Behavior:** The agent's behavior, personality, and components are all defined in a central `settings.yaml` file, making it highly customizable.
- **Persistent Memory:** Supports both short-term (session) and long-term (persistent) memory, allowing the agent to recall past interactions.
- **Extensible:** Designed to be easily extended with new agents, tools, and connections to different AI models (OpenAI, Gemini, Claude).

## 3. System Architecture Overview

The system is designed around a central `CoreAgent` that acts as the brain. When a user provides input, the `CoreAgent` processes it and routes the request to the most appropriate specialized agent.

1.  **Input Handling:** The `main.py` entry point starts the `CoreAgent`.
2.  **Orchestration:** The `CoreAgent` receives the user input, stores it in short-term memory, and then decides which sub-agent to use.
3.  **Delegation:** The request is passed to a specialized agent (e.g., `ToolAgent` for API calls, `TaskAgent` for to-do list management).
4.  **Execution:** The specialized agent performs its function, potentially using tools from the `tools/` directory.
5.  **Response Generation:** The result is returned to the `CoreAgent`, which stores it in memory and styles it according to the defined `Personality`.
6.  **Output:** The final, styled response is delivered to the user.

## 4. Folder and File Explanations

```
/trial-ai-agent-1
│
├── agent/
│   ├── core_agent.py          # Central decision-making unit
│   ├── personality.py         # Communication & response rules
│   ├── memory.py              # Memory storage & retrieval
│   └── agent_manager.py       # Sub-agent lifecycle management
│
├── agents/
│   ├── chat_agent.py          # Conversational logic
│   ├── voice_agent.py         # Speech-to-text and text-to-speech (simulated)
│   ├── tool_agent.py          # API and tool execution
│   └── task_agent.py          # Task planning & execution logic
│
├── tools/
│   ├── api_tools.py           # External API connectors (simulated)
│   ├── system_tools.py        # Local system operations (safe)
│
├── memory_store/
│   ├── short_term.json        # Session-based memory
│   └── long_term.json         # Persistent memory
│
├── config/
│   └── settings.yaml          # Models, rules, and system configuration
│
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── README.md                  # This documentation
└── LICENSE                    # Project license
```

## 5. How the Agent Works Internally

The agent's intelligence is distributed across its components:

-   **`CoreAgent`**: The central orchestrator. It doesn't perform tasks itself but intelligently routes them. The current routing logic is keyword-based but is designed to be replaced by an LLM for more advanced intent recognition.
-   **`AgentManager`**: Dynamically loads the sub-agents specified in `settings.yaml`. This allows developers to add or remove agents without touching the core logic.
-   **Specialized Agents**: Each agent in the `agents/` directory has a single responsibility. For example, `ToolAgent` knows how to use tools, while `ChatAgent` knows how to hold a conversation.
-   **Tools**: Tools are simple Python classes that perform a single, specific action, like fetching the weather or getting the time. This makes them reusable and easy to test.
-   **Memory**: The `Memory` class uses JSON files to simulate a database. It saves the conversation history, which can be used to provide context for future interactions.

## 6. Installation and Usage

Follow these steps to get the AI Agent running on your local machine.

### Prerequisites

-   Python 3.8 or higher
-   `pip` for package management

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/trial-ai-agent-1.git
    cd trial-ai-agent-1
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

### Usage

1.  **Run the agent from the command line:**
    ```sh
    python main.py
    ```

2.  **Interact with the agent:**
    Once the agent is running, you can type your requests directly into the console. Try the following commands:
    -   `hello`
    -   `tell me a joke`
    -   `what time is it?`
    -   `what is the weather in Paris?`
    -   `remind me to call the doctor`
    -   `what are my tasks`
    -   `exit` (to end the session)

## 7. Future Roadmap

This project provides a solid foundation. Future enhancements could include:

-   **LLM-Powered Routing:** Replace the simple keyword-based routing in `CoreAgent` with a language model to better understand user intent.
-   **Real Voice Integration:** Integrate actual Speech-to-Text and Text-to-Speech libraries (e.g., `SpeechRecognition`, `gTTS`).
-   **Advanced Memory Management:** Implement a more sophisticated memory system, possibly using a vector database for semantic search over past conversations.
-   **Dynamic Tool Creation:** Allow the agent to write its own tools (e.g., Python scripts) to solve novel problems.
-   **GUI Interface:** Build a graphical user interface (GUI) using a framework like Tkinter, PyQt, or a web-based interface.
-   **Containerization:** Dockerize the application for easier deployment and scalability.

## 8. Credits

© Aditya Pratap
