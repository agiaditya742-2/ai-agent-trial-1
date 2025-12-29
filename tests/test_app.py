import unittest

class TestAppStructure(unittest.TestCase):

    def test_app_creation(self):
        """
        Test that the Flask application can be created without errors.
        """
        try:
            from app.main import create_app
            app = create_app()
            self.assertIsNotNone(app)
        except Exception as e:
            self.fail(f"Flask app creation failed with an exception: {e}")

    def test_agent_imports(self):
        """
        Test that all core agent modules can be imported without errors.
        """
        try:
            from app.agent.core_agent import CoreAgent
            from app.agent.memory import Memory
            from app.agent.personality import Personality
            from app.agents.chat_agent import ChatAgent
            from app.agents.tool_agent import ToolAgent
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import a core agent module: {e}")

if __name__ == '__main__':
    unittest.main()
