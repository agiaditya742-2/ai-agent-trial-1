from flask import Flask
import os

def create_app():
    """
    Application factory for the Flask app.
    Initializes the Flask app, configures it, and registers blueprints.
    """
    # Note the template_folder path is relative to the app package
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # --- Configuration ---
    # Set a default upload folder. The path should be absolute or relative to the instance folder.
    # We'll create the folder if it doesn't exist.
    UPLOAD_FOLDER = os.path.join(app.instance_path, 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    app.config.from_mapping(
        SECRET_KEY='dev', # Change for production
        UPLOAD_FOLDER=UPLOAD_FOLDER,
    )

    # --- Register Blueprints ---
    from .routes import main_bp
    app.register_blueprint(main_bp)

    # --- (Future) Initialize Extensions ---
    # e.g., db.init_app(app)

    return app
