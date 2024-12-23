import os
import importlib.util
from utils import get_logger

logger = get_logger()

class ActionWorker:
    def __init__(self):
        self.action_map = {}
        self.load_utils(os.getcwd() + "/src/machine_interface/utils")

    def load_utils(self, utils_folder):
        if not os.path.isdir(utils_folder):
            logger.error(f"Utils folder '{utils_folder}' not found!")
            return

        for file_name in os.listdir(utils_folder):
            if file_name.endswith(".py") and "TEMPLATE.py" not in file_name:
                module_name = file_name[:-3]  # Strip `.py`
                file_path = os.path.join(utils_folder, file_name)

                # Import the module dynamically
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Map functions in the module to the action_map
                for attr_name in dir(module):
                    if not attr_name.startswith("_"):  # Skip private/internal attributes
                        func = getattr(module, attr_name)
                        if callable(func):
                            action_name = f"{module_name}"
                            self.action_map[action_name] = func
                            logger.success(f"Loaded action: {action_name}")

    def run(self, action: str, parameters: dict) -> str:
        if action in self.action_map:
            try:
                return self.action_map[action](**parameters)
            except TypeError as e:
                logger.error(f"Error executing action '{action}': {e}")
        else:
            logger.error(f"Invalid action: {action}")

    