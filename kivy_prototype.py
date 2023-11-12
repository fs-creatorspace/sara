import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from conversation import Conversation  # Import the Conversation class from your module

class ChatBotApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.output_label = Label(text="ChatBot Output:")
        self.layout.add_widget(self.output_label)

        self.conversation = Conversation(path="conversation_data", load=0)  # Create an instance of the Conversation class

        # Create a button to call the textToSpeech function
        self.text_to_speech_button = Button(text="Text to Speech")
        self.text_to_speech_button.bind(on_press=self.text_to_speech)
        self.layout.add_widget(self.text_to_speech_button)

        # Create a button to call the speak function
        self.speak_button = Button(text="Speak")
        self.speak_button.bind(on_press=self.speak)
        self.layout.add_widget(self.speak_button)

        return self.layout

    def text_to_speech(self, instance):
        # Example: Call the textToSpeech function from the Conversation class
        question = "Hello, this is a test question."
        audio_path = self.conversation.textToSpeech(question)
        self.output_label.text = f"Text to Speech function called. Audio saved at {audio_path}"

    def speak(self, instance):
        # Example: Call the speak function from the Conversation class
        audio_path = "path_to_audio.mp3"  # Replace with the actual path to an audio file
        self.conversation.speak(audio_path)
        self.output_label.text = "Speak function called."

if __name__ == '__main__':
    ChatBotApp().run()
