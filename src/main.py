from human_interface import SpeechWorker, SpeechToText, BrowserHandler
from llm_interface import OllamaLLM
from machine_interface import ActionWorker
import os

def main():
    OllamaLLM(
        speech_worker=SpeechWorker(),
        speech_to_text_worker=SpeechToText(),
        action_worker=ActionWorker(),
        browser=BrowserHandler(driver_path=os.getcwd()+"\\src\\human_interface\\chromedriver\\chromedriver.exe", browser_url="https://duckduckgo.com/")
    ).launch()

if __name__ == "__main__":
    main()