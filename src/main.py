from human_interface import SpeechWorker
from llm_interface import OllamaLLM

def main():
    OllamaLLM(
        speech_worker=SpeechWorker()
    ).launch()

if __name__ == "__main__":
    main()