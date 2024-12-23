from human_interface import SpeechWorker, SpeechToText
from llm_interface import OllamaLLM
from machine_interface import ActionWorker

def main():
    OllamaLLM(
        speech_worker=SpeechWorker(),
        speech_to_text_worker=SpeechToText(),
        action_worker=ActionWorker()
    ).launch()

if __name__ == "__main__":
    main()