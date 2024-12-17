from human_interface import SpeechTask, SpeechWorker
import threading
import time

def main():
    speech_worker = SpeechWorker()
    speech_worker.start()
    speech_worker.add_task_to_queue("Hey this is a speech related task")
    speech_worker.stop()
    while True:
        pass
    
if __name__ == "__main__":
    main()