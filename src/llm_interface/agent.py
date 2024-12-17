import subprocess
import sys
import shutil
import json

class OllamaLLM():
    def __init__(self, speech_worker=None):
        self._running_state = False
        self._speech_worker = speech_worker

    def launch(self):
        if shutil.which("ollama") is None:
            print("Error: 'ollama' command not found. Please install ollama.")
            sys.exit(1)
        if self._speech_worker is None:
            print("Starting agent without speech disabled")
        else:
            self._speech_worker.start()
        self.start_ollama()
        # Interact with the model
        self.interact_with_model()
        
    def run_ollama_command(self, command, capture_output=True):
        print(f"Running command: {command}")
        result = subprocess.run(command, shell=True, text=True, capture_output=capture_output)
        if capture_output:
            return result.stdout.strip()
        else:
            return result

    def start_ollama(self):
        """Pull the model, create it, and run it."""
        print("Pulling the llama3.1 model...")
        self.run_ollama_command("ollama pull llama3.1")
        
        print("Creating the model 'frank' from Modelfile...")
        self.run_ollama_command("ollama create frank -f ./Modelfile")
        
        print("Running the 'frank' model...")
        self.run_ollama_command("ollama run frank")

    def interact_with_model(self):
        """Interact with the 'frank' model by sending text input and getting output."""
        print("Type your input to send to the model (type 'exit' to quit):")
        
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Exiting...")
                break
            
            # Send the user input to ollama and capture the output
            command = f"echo '{user_input}' | ollama run frank"
            output = self.run_ollama_command(command, capture_output=True)
            print(output)
            self._speech_worker.add_task_to_queue(json.loads(output)["speak"])
    
    def shutdown(self):
        self._speech_worker.stop()