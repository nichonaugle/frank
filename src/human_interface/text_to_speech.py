from colorama import Fore, Style
import pyttsx3
import time
import threading
import queue

class SpeechTask:
    def __init__(self, text):
        self.text = text
        self.completed = threading.Event()  # Event to signal task completion
        self.result = None  # To hold the task's result (e.g., success or failure)

    def run(self):
        """Execute the speech task."""
        try:
            # Create a new engine instance for this task
            engine = pyttsx3.init()
            engine.say(self.text)
            engine.runAndWait()  # Blocking call, specific to this task instance
            self.result = "Success"
        except Exception as e:
            self.result = f"Failed: {e}"
            print(f"{Fore.RED}[Speaking]{Style.RESET_ALL} Error during speech task: {e}")
        finally:
            # Signal that the task is complete
            self.completed.set()
            # Clean up the engine (optional, but good practice)
            del engine

    def wait_for_completion(self):
        """Wait for the task to finish."""
        self.completed.wait()
        return self.result

class SpeechWorker:
    """A worker that processes speech tasks indefinitely from a queue."""
    def __init__(self):
        self.task_queue = queue.Queue()
        self.stop_signal = threading.Event()  # Used to stop the worker if needed
        self.worker_thread = threading.Thread(target=self.runner, daemon=True)
        self.running_lock = threading.Lock()  # Mutex for managing `running` state

    def start(self):
        self.worker_thread.start()
        # Needed to preload the threading engine otherwise there is a large delay
        self.add_task_to_queue("Launching Speech Engine")
        time.sleep(0.5)

    def runner(self):
        """Worker thread function that processes tasks from the queue."""
        print(f"{Fore.GREEN}[INFO]{Style.RESET_ALL} Speech worker started. Ready for tasks...")
        while not self.stop_signal.is_set():
            try:
                # Get a new task; blocks until a task is available
                text = self.task_queue.get()
                self.running_lock.acquire()
                if text is None:
                    # If a None task is received, stop the worker
                    print(f"{Fore.GREEN}[INFO]{Style.RESET_ALL} Stopping worker...")
                    break
                print(f"{Fore.CYAN}[Speaking]{Style.RESET_ALL} '{text}'")
                result = self.execute_speech_task(text).wait_for_completion()
                self.task_queue.task_done()
                self.running_lock.release()
            except Exception as e:
                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Error during speech task: {e}")

    def execute_speech_task(self, text):
        task = SpeechTask(text)
        threading.Thread(target=task.run, daemon=True).start()
        return task

    def add_task_to_queue(self, text):
        """Add a new speech task to the queue."""
        if self.worker_thread.is_alive():
            self.task_queue.put(text)
        else: 
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} SpeechWorker thread is not running. Tasks cannot be added until SpeechWorker is started")

    def running_tasks(self):
        if self.running_lock.locked() or not self.task_queue.empty():
            return True
        return False
    
    def stop(self):
        """Gracefully stop the worker."""
        self.task_queue.join()
        self.stop_signal.set()
        self.task_queue.put(None)  # Add a stop task to unblock the worker thread
        self.worker_thread.join()