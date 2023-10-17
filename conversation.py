import openai
import speech_recognition as sr
import gtts
from dotenv import load_dotenv
import pygame.mixer
import os
import re

class Conversation():
    def __init__(self, path: str, load = 0):

        self.audio_storage = []
        self.transcript_storage = []
        self.summary_storage = []
        self.question_storage = []

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
            print(f"Path not found. Creating {path}")
            os.mkdir(path)

        # Getting List of all folders
        folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        
        # Extract the numbers at the end of the folder names, convert them to integers, and find the maximum
        folder_numbers = [int(f.split("_")[1]) for f in folders]
        
        # Set to highest
        if folder_numbers:
            self.id = max(folder_numbers) + 1
        else: self.id = 1

        os.mkdir(path + f"/conv_{self.id}")

        print(f"Setting up conversation {self.id}")
        
        self.recognizer = sr.Recognizer()

        # Setup environment variables
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def record(self) -> sr.AudioData:
        # Starts listening to user input and returns an audio data object from recognizer
        # Saves wav to audio_storage
        return
    
    def speechToText(self, audioData: sr.AudioData) -> str:
        # Recieves audio data object and returns a transcript
        # Saves transcript to transcript_storage
        return
    
    def summarize(self, text: str) -> str:
        # Recieves raw text, refines grammar and summarizes it
        # Saves summary to summary_storage
        return
    
    def generateQuestion(self) -> str:
        # Takes all summaries and all questions and generates a new question with use of LLM
        # Saves new question to question_storage
        return
    
    def textToSpeech(self, question: str) -> str:
        # Takes question and saves it as mp3 audio. Returns path to mp3 file
        return

    def speak(self, path: str):
        # Plays mp3 file from path
        return

