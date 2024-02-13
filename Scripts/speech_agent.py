import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig, SpeechSynthesisOutputFormat, SpeechSynthesizer, ResultReason, CancellationReason
from dotenv import load_dotenv

load_dotenv()

class SpeechAgent:
    def __init__(self):
        self.speech_config = SpeechConfig(subscription=os.getenv("AZURE_SPEECH_KEY"), region=os.getenv("AZURE_SPEECH_REGION"))
        self.speech_config.speech_synthesis_voice_name = 'en-US-AvaMultilingualNeural'
        self.audio_config = AudioConfig(use_default_microphone=True)
        self.speech_recognizer = None
        self.is_recognizing = False
        self.last_heard_time = None
        self.silence_threshold = None

    def start_recognition(self):
        print("Listening...")
        self.speech_recognizer = SpeechRecognizer(speech_config=self.speech_config, audio_config=self.audio_config)
        result = self.speech_recognizer.recognize_once_async().get()
        self.is_recognizing = True
        print(f"Speech result: {result.text}")
        return result.text

    def stop_recognition(self):
        if self.speech_recognizer:
            print("Stopping recognition...")
            self.speech_recognizer.stop_continuous_recognition()
            self.speech_recognizer = None
        self.is_recognizing = False

    def synthesize_speech(self, text):
        speech_synthesizer = SpeechSynthesizer(speech_config=self.speech_config)
        result = speech_synthesizer.speak_text_async(text).get()
        return result
