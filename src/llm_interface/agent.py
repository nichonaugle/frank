import subprocess
import sys
import shutil
import json
from ollama import chat
import time
import os
import ast
from utils import get_logger

logger = get_logger()

class OllamaLLM():
    def __init__(self, speech_worker=None, action_worker=None, speech_to_text_worker=None):
        self._running_state = False
        self._speech_worker = speech_worker
        self._speech_to_text_worker = speech_to_text_worker
        self._action_worker = action_worker
        self._communication_process = None
        self._chat_history = []

    def launch(self):
        try:
            if shutil.which("ollama") is None:
                logger.critical("Error: 'ollama' command not found. Please install ollama.")
                sys.exit(1)
            if self._speech_worker is None:
                logger.warning("Starting agent without speech disabled")
            else:
                self._speech_worker.start()
            if self._action_worker is None:
                logger.error("Error: No action worker provided. Nothing will happen")
                sys.exit(1)
            self.setup_ollama_and_modelfile()
            self.interaction_portal()
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt is stopping program")
        except Exception as err:
            logger.critical(f"Unknown error occured: {err}")
        finally:
            self.shutdown()

    def run_ollama_command(self, command):
        response = chat(
            'frank',
            messages=self._chat_history
            + [
                {'role': 'user', 'content': command},
            ],
        )
        self._chat_history += [
            {'role': 'user', 'content': command},
            {'role': 'assistant', 'content': response.message.content},
        ]
        return response

    def setup_ollama_and_modelfile(self):
        """Pull the model, create it, and run it."""
        logger.info("Pulling the llama3.1 model...")
        logger.debug(subprocess.run("ollama pull llama3.1", shell=True, text=True))
        
        logger.info("Creating the model 'frank' from Modelfile...")
        logger.debug(subprocess.run(f"ollama create frank -f {os.getcwd() + '/Modelfile'}", shell=True, text=True))
    
    def interaction_portal(self):
        logger.info("Opening interaction portal")
        action_result = "None"
        while True:
            try:
                if action_result == "None" or action_result == None:
                    if self._speech_to_text_worker is None:
                        user_input = input("You: ")
                    else:
                        while self._speech_worker.running_tasks():
                            time.sleep(1) # just a tiny delay
                        logger.success("Please say your command: ")
                        user_input = self._speech_to_text_worker.recognize_speech()
                        logger.sent(f"'{user_input}'")

                    if user_input == None or user_input.lower() == "exit":
                        logger.info("Exiting...")
                        break
                else:
                    user_input = action_result
                # Send the user input to ollama and capture the output
                output = self.run_ollama_command(user_input)
                response_content = ast.literal_eval(output.message.content.strip()) # Now a python dict
                action = response_content["action_name"]
                parameters = response_content["parameters"]
                logger.recieved(f"action_name='{action}' | parameters={parameters}")
                
                # If action or parameters are invalid, reset action_result
                if not action:
                    action_result = "You either didnt say anothing or formatted it wrong. Try again"
                elif action == "wait_for_human_input":
                    action_result = "None"
                elif action == "speak":
                    content = parameters["content"]
                    if content:
                        self._speech_worker.add_task_to_queue(content)
                        action_result = "Successfully spoke content. If you finished running your commands please return the wait for human input command"
                    else:
                        action_result = "Error: Missing 'content' in 'parameters'"
                else:
                    action_result = self._action_worker.run(action, parameters)
            except (SyntaxError, ValueError) as e:
                logger.error(f"Error parsing string: {e}")
                logger.error(f"Error: Failed to decode JSON response: {output.message.content.strip()}")
                action_result = "Error: Failed to decode JSON response. You either formatted it wrong or need to run command again."
            except KeyError as e:
                logger.error(f"Error: Missing expected key {e}")
                action_result = e
            except Exception as err:
                logger.error(f"Unhandled error: {err}")
                action_result = err
                break

    def shutdown(self):
        self._speech_worker.stop()