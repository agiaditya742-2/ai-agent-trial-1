from flask import Blueprint, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os

from .extensions import agent

main_bp = Blueprint('main_bp', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    response = agent.process(user_input)
    return jsonify({'response': response})

@main_bp.route('/history', methods=['GET'])
def history():
    return jsonify(agent.memory.get_history())

@main_bp.route('/upload', methods=['POST'])
def upload_file():
    # This needs access to app.config, which we will fix during refactoring
    from flask import current_app

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        try:
            content = ""
            if filename.lower().endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif filename.lower().endswith('.pdf'):
                content = "PDF content would be extracted here."

            agent.memory.add_to_short_term(f"system: Ingested content from {filename}: {content[:500]}...")

            return jsonify({'response': f'File {filename} uploaded and ingested successfully.'})
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500

    return jsonify({'error': 'File type not allowed'}), 400
