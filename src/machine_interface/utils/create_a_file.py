def run(file_path: str) -> str:
    import os
    
    try:
        # Ensure the model gave the right output
        if not file_path.startswith("/franksfolder/"):
            return "You did not provide the directory path correctly. Please prefix your path with '/franksfolder/'"

        # Get the full path relative to the current working directory
        full_path = os.getcwd() + file_path

        # Split the file path into directory and file name
        directory = os.path.dirname(full_path)

        # Ensure the directory exists
        if not os.path.exists(directory):
            os.makedirs(directory)  # Create necessary directories

        # Create the file
        with open(full_path, "w") as file:
            pass  # Create an empty file

        return f"File created successfully at: {file_path}"
    except Exception as e:
        return f"Failed to create file at {file_path}: {e}"
