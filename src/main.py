from human_interface import SpeechWorker
from llm_interface import OllamaLLM
from machine_interface import ActionWorker

def main():
    """
    action_worker=ActionWorker()
    print(action_worker.run("read_a_file", {"file_path": "/franksfolder/test.txt"}))
    """
    OllamaLLM(
        speech_worker=SpeechWorker(),
        action_worker=ActionWorker()
    ).launch()

if __name__ == "__main__":
    main()