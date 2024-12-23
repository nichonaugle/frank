import speech_recognition as sr
from utils import get_logger

logger = get_logger()

class SpeechToText:
    def __init__(self):
        self.r = sr.Recognizer()
        self._mic = sr.Microphone()
        with self._mic as source:
            self.r.adjust_for_ambient_noise(source)
        self.r.pause_threshold = 1.5

    def recognize_speech(self) -> str:
        try:
            while True:
                with self._mic as source:
                    audio = self.r.listen(source)
                    try:
                        return self.r.recognize_google(audio)
                    except sr.UnknownValueError:
                        logger.warning('Google Speech Recognition could not understand your audio')
                        #pass
                    except sr.RequestException as e:
                        logger.warning(f'Speech recognition error: {e}')
                        #pass

        except KeyboardInterrupt:
            logger.info("Clean exit...")
            pass

        except Exception as err:
            logger.error(f"Error occured: {err}")