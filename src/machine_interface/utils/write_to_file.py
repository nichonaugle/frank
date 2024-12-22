def run(file_path: str, content: str) -> str:
    import os

    try:
        # Ensure the file path starts with the required prefix
        if not file_path.startswith("/franksfolder/"):
            return "You did not provide the directory path correctly. Please prefix your path with '/franksfolder/'"

        # Get the full path relative to the current working directory
        full_path = os.path.join(os.getcwd(), file_path.lstrip("/"))

        # Split the file path into directory and file name
        directory = os.path.dirname(full_path)

        # Ensure the directory exists
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Write content to the file, handling newlines and carriage returns
        if content == "":
            return f"No content provided to write to {file_path} so nothing was written."
        
        normalized_content = content.replace("\r\n", "\n").replace("\r", "\n")
        
        with open(full_path, "w") as file:
            file.write(normalized_content)

        return f"File created successfully at: {file_path}"

    except Exception as e:
        return f"Failed to create file at {file_path}: {e}"
