# server.py

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from agent.core_agent import CoreAgent
import PyPDF2
import io

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

# --- API Route for Getting History ---
@app.route('/history', methods=['GET'])
def history():
    """
    Provides the current conversation history.
    """
    if not agent:
        return jsonify({"error": "The AI agent is not available."}), 500

    return jsonify({"history": agent.memory.get_conversation_history()})

# --- API Route for Clearing Memory ---
@app.route('/clear_memory', methods=['POST'])
def clear_memory():
    """
    Clears the agent's short-term conversation history.
    """
    if not agent:
        return jsonify({"error": "The AI agent is not available."}), 500

    agent.memory.clear_short_term_memory()
    return jsonify({"status": "success", "message": "Conversation history cleared."})

@app.route('/feed', methods=['POST'])
def feed_agent():
    """
    Allows feeding the agent new knowledge from text or PDF files.
    """
    if not agent:
        return jsonify({"error": "The AI agent is not available."}), 500

    text_data = request.form.get('text')
    file = request.files.get('file')

    knowledge_source = "unknown"

    if file:
        filename = file.filename
        knowledge_source = f"file: {filename}"
        content = ""
        if filename.lower().endswith('.pdf'):
            try:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
                for page in pdf_reader.pages:
                    content += page.extract_text()
                # Simulate RAG by adding a summary to long-term memory
                summary = f"The user uploaded a PDF named '{filename}'. Key content includes: {content[:200]}..."
                agent.memory.add_entity_to_long_term("document_knowledge", {filename: summary})

            except Exception as e:
                return jsonify({"error": f"Failed to process PDF: {e}"}), 400
        else:
            # Handle other file types, like .txt
            content = file.read().decode('utf-8')
            summary = f"The user uploaded a file named '{filename}'. Key content includes: {content[:200]}..."
            agent.memory.add_entity_to_long_term("document_knowledge", {filename: summary})

    elif text_data:
        knowledge_source = "direct text"
        summary = f"The user provided text data. Key content includes: {text_data[:200]}..."
        agent.memory.add_entity_to_long_term("text_knowledge", {"user_text_feed": summary})

    else:
        return jsonify({"error": "No text or file provided."}), 400

    return jsonify({"status": "success", "message": f"Knowledge from {knowledge_source} has been fed to the agent."})

# --- Advanced Feature Routes ---

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # In a real app, save the file securely and pass its info to the agent
    # For now, we'll just acknowledge the upload
    filename = file.filename
    # This is a placeholder for where file handling logic would go.
    # For now, we just add a message to the conversation.
    response_message = f"I've received the file '{filename}'. How can I help you with it?"
    agent.memory.add_to_short_term({"role": "assistant", "content": response_message})

    return jsonify({"response": response_message})

@app.route('/deep_thinking', methods=['POST'])
def set_deep_thinking():
    data = request.json
    mode = data.get('enabled', False)
    result = agent.toggle_deep_thinking(mode)
    return jsonify(result)

@app.route('/autonomous/start', methods=['POST'])
def start_autonomous():
    data = request.json
    goal = data.get('goal')
    if not goal:
        return jsonify({"error": "A goal is required to start autonomous mode."}), 400
    result = agent.start_autonomous_mode(goal)
    return jsonify(result)

@app.route('/autonomous/stop', methods=['POST'])
def stop_autonomous():
    result = agent.stop_autonomous_mode()
    return jsonify(result)

@app.route('/autonomous/status', methods=['GET'])
def autonomous_status():
    status = agent.get_autonomous_status()
    return jsonify(status)

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
