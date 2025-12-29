
import os
import json

# --- Simulated File System Operations ---

def create_file(file_path: str, content: str = ""):
    """
    Simulates creating a file with specified content.
    For safety, this operates in a sandboxed 'desktop' directory.
    """
    sandbox_dir = "desktop_sandbox"
    if not os.path.exists(sandbox_dir):
        os.makedirs(sandbox_dir)

    full_path = os.path.join(sandbox_dir, file_path)

    try:
        with open(full_path, 'w') as f:
            f.write(content)
        return json.dumps({"status": "success", "message": f"File '{file_path}' created in sandbox."})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def read_file(file_path: str):
    """
    Simulates reading a file from the sandbox directory.
    """
    sandbox_dir = "desktop_sandbox"
    full_path = os.path.join(sandbox_dir, file_path)

    try:
        with open(full_path, 'r') as f:
            content = f.read()
        return json.dumps({"status": "success", "content": content})
    except FileNotFoundError:
        return json.dumps({"status": "error", "message": "File not found."})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def list_files(directory: str = "."):
    """
    Simulates listing files in a specified directory within the sandbox.
    """
    sandbox_dir = "desktop_sandbox"
    target_dir = os.path.join(sandbox_dir, directory)

    if not os.path.exists(target_dir):
        return json.dumps({"status": "error", "message": "Directory not found."})

    try:
        files = os.listdir(target_dir)
        return json.dumps({"status": "success", "files": files})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

# --- (You can add other simulated system tools here) ---
