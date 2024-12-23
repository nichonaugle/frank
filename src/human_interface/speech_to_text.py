import speech_recognition as sr

class SpeechToText:
    def __init__(self):
        self.r = sr.Recognizer()

    def recognize_speech(self) -> str:
        try:
            with sr.Microphone() as source:
                audio = self.r.listen(source)
                try:
                    return self.r.recognize_google(audio)
                except sr.UnknownValueError:
                    print('Google Speech Recognition could not understand your audio')
                    pass
                except sr.RequestException as e:
                    print(f'Speech recognition error: {e}')
                    pass

        except KeyboardInterrupt:
            print("Clean exit...")
            pass

        except Exception as err:
            print(f"Error occured: {err}")