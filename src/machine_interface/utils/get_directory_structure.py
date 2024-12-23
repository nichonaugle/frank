def run(file_path: str) -> str:
    """
    Recursively retrieves a folder and its nested files in a structure
    suitable for LLMs to understand.

    Args:
        directory_path (str): The path to the directory.

    Returns:
        str: A string representation of the folder structure.
    """
    import os
    import json

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
            return directory + " does not exist. Please prefix your path with '/franksfolder/'" # Create necessary directories

        # Parse the directory
        def parse_directory(dir):
            structure = {}
            for entry in os.listdir(dir):
                full_path = os.path.join(dir, entry)
                if os.path.isdir(full_path):
                    structure[entry] = parse_directory(full_path)
                else:
                    structure[entry] = "file"
            return structure
        
        folder_structure = {"directory": file_path, "structure": parse_directory(directory)}
        return json.dumps(folder_structure, indent=2)
    
    except Exception as e:
        return {"Error thrown while trying to create the directory structure: ": str(e)}
