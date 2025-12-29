# This file is used to initialize extensions and other components
# that need to be shared across the application, avoiding circular imports.

from app.agent.memory import Memory
from app.agent.core_agent import CoreAgent

# Adjust paths to reflect the new 'app/' directory structure
memory = Memory(
    short_term_file='app/memory_store/short_term.json',
    long_term_file='app/memory_store/long_term.json'
)

# The agent is instantiated here once and can be imported by other modules
agent = CoreAgent(memory)
