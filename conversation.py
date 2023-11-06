import openai
import speech_recognition as sr
import gtts
from dotenv import load_dotenv
import pygame.mixer
import os
import re

class Conversation():
    def __init__(self, path: str, load = 0):
        
        self.path = path
        self.conv_counter = 0
        self.recognizer = sr.Recognizer()
        
        self.question_storage = []
        self.audio_storage = []
        self.transcript_storage = []
        self.summary_storage = []

        if load:
            self.id = load
            # TBD
            # Load all data from folder
        else:
            # TBD
            # Load random start question
            self.question_storage.append("How did you meet your first love?")
            pass

        if not os.path.isdir(path):
            print(f"/{path} not found. Creating /{path}")
            os.mkdir(path)

        # Getting List of all folders
        folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        
        # Extract the numbers at the end of the folder names, convert them to integers, and find the maximum
        folder_numbers = [int(f.split("_")[1]) for f in folders]
        
        # Set to highest
        if folder_numbers:
            self.id = max(folder_numbers) + 1
        else: self.id = 1

        print(f"Setting up conversation {self.id}")
        os.mkdir(path + f"/conv_{self.id}")
        
        self.recognizer = sr.Recognizer()

        # Setup environment variables
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")


    def textToSpeech(self, question: str) -> str:
        """ 
        Takes question and saves it as mp3 audio. Returns path to mp3 file 

        Args:
            question (str): The question to be converted to speech

        Returns:
            str: The path to the saved mp3 file
        """
        
        # Convert text to speech
        tts = gtts.gTTS(text=question, lang='en')
        path = f"{self.path}/conv_{self.id}/question_{self.conv_counter}.mp3"
        tts.save(path)
        return path
    

    def speak(self, path: str):
        # Plays mp3 file from path
        absolute_path = os.path.abspath(path)
        if os.path.exists(absolute_path):
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(absolute_path)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            except KeyboardInterrupt:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                print("Playback stopped and resources released.")
            pygame.mixer.quit()
        else:
            print(f"File {absolute_path} does not exist!")

    def record(self) -> sr.AudioData:
        # Starts listening to user input and returns an audio data object from recognizer
        # Saves wav as a new file in conversation folder (NOT IN audio_storage!!)
        
        with sr.Microphone() as source:
            print("Please speak something...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio_data = self.recognizer.listen(source)
            print("Recognizing...")

            try:
                # Get WAV data from captured audio
                wav_data = audio_data.get_wav_data()
                
                # Save the WAV data to a file
                with open(f"{self.path}/conv_{self.id}/answer_{self.conv_counter}.wav", 'wb') as file:
                    file.write(wav_data)
                print("Audio saved to captured_audio.wav")

            except sr.UnknownValueError:
                text = "UnknownValueError"   #REMOVE THIS LATER!!!!!!!!!!!!
                print("I not understand the audio.")
            except sr.RequestError:
                print("API Error.")
        
        return audio_data
    
    
    def speechToText(self, audioData: sr.AudioData = None, bypass = "") -> str:
        # Recieves audio data object and returns a transcript
        # Saves transcript to transcript_storage

        if bypass:
            text = bypass
        else:
            text = self.recognizer.recognize_google(audioData)
        print(f"You said: {text}")
        self.transcript_storage.append(text)
        return text
    
    def summarize(self, text: str) -> str:
        # Recieves raw text, refines grammar and summarizes it
        # Saves summary to summary_storage
        messages = [
        {"role": "system", "content": "You are a helpful assistant focussing on receiving a good story."},
        {"role": "user", "content": f"Provide a brief summary of the following text and correct any grammar mistakes/wrong words. Dont change the meaning of the text.: '{text}'"}
        ]
    
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

        summary_q = response.choices[0].message['content'].strip()
        self.summary_storage.append(summary_q)
        return summary_q
    
    def generateQuestion(self) -> str:
        # Takes all summaries and all questions and generates a new question with use of LLM
        # Saves new question to question_storage
        messages = [
        {"role": "system", "content": "You are a helpful assistant that asks questions relevant to a story."},
        {"role": "user", "content": f"You are given a summary of a previously asked questions. Ask a relevant follow up Question (that has not been asked before) to get more relevant information about the summary. Use simple Vocabulary and talk like you are in a real conversation: Questions: '{self.question_storage}' Summary:'{self.summary_storage}'"}
        ]
    
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

        follow_up_q = response.choices[0].message['content'].strip()
        self.question_storage.append(follow_up_q)
        return follow_up_q

    def showHistory(self):
        # prints out the question_storage and summary_storage
        print("Questions:")
        for idx, q in enumerate(self.question_storage):
            print(f"{idx}: {q}")
        
        print("----------")
        print("Summaries:")
        for idx, s in enumerate(self.summary_storage):
            print(f"{idx}: {s}")
