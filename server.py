# server.py

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from agent.core_agent import CoreAgent

# Initialize the Flask application
app = Flask(__name__, static_folder='webapp')

# Enable Cross-Origin Resource Sharing (CORS) to allow the frontend
# to make requests to this server from a different origin.
CORS(app)

# --- Initialize the AI Agent ---
# We create a single, persistent instance of the CoreAgent so that it
# retains its memory and state throughout the life of the server.
print("Initializing CoreAgent for the web server...")
try:
    agent = CoreAgent()
    print("CoreAgent initialized successfully.")
except Exception as e:
    print(f"FATAL: Failed to initialize CoreAgent. Error: {e}")
    # If the agent can't be created, there's no point in running the server.
    agent = None

# --- API Route for Chatting ---
@app.route('/chat', methods=['POST'])
def chat():
    """
    The main API endpoint for communicating with the AI agent.

    This endpoint accepts a JSON payload with a "message" field and
    returns the agent's response.
    """
    if not agent:
        return jsonify({"error": "The AI agent is not available."}), 500

    # Get the user's message from the request body
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided."}), 400

    # Process the message through the agent's handler
    try:
        agent_response = agent.handle_request(user_message)
        return jsonify({"response": agent_response})
    except Exception as e:
        print(f"An error occurred while handling a request: {e}")
        return jsonify({"error": "An internal error occurred."}), 500

# --- Route for Serving the Frontend ---
@app.route('/')
def serve_webapp():
    """
    Serves the main `index.html` file of the web application.
    """
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """
    Serves other static files (like CSS and JS) from the `webapp` directory.
    """
    return send_from_directory(app.static_folder, path)

# --- Main Entry Point ---
if __name__ == '__main__':
    # Starts the Flask development server.
    # In a production environment, you would use a more robust server like Gunicorn.
    print("Starting the Flask server...")
    # The host '0.0.0.0' makes the server accessible from other devices on the network.
    app.run(host='0.0.0.0', port=5000, debug=True)
