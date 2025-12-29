# This is the single entry point for the application.
from app.main import create_app

app = create_app()

if __name__ == '__main__':
    # The host must be 0.0.0.0 to be accessible from outside the container
    app.run(host='0.0.0.0', port=5000, debug=True)
