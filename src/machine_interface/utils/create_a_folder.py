def run(file_path: str) -> str:
    import os
    
    try:
        # Ensure the model gave the right output
        if not file_path.startswith("/franksfolder/"):
            return "You did not provide the directory path correctly. Please prefix your path with '/franksfolder/'"

        if "." in file_path.split("/")[-1]:
            return "You did not provide the directory path correctly. Please remove the file name and create the folder first."
        # Get the full path relative to the current working directory
        if not file_path.endswith("/"):
            file_path = file_path + "/"

        full_path = os.getcwd() + file_path
        # Split the file path into directory and file name
        directory = os.path.dirname(full_path)

        # Create the file
        os.makedirs(directory, exist_ok=True)

        return f"Directory created successfully at: {directory}"
    except Exception as e:
        return f"Error creating directory at {directory}: {str(e)}"

