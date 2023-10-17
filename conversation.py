import openai
import speech_recognition as sr
import gtts
from dotenv import load_dotenv
import pygame.mixer
import os
import re

def Conversation():
    def __init__(self, path: str):

        # Getting List of all folders
        folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        # Extract the numbers at the end of the folder names, convert them to integers, and find the maximum
        folder_numbers = [int(re.search(r'\d+$', folder).group()) for folder in folders if re.search(r'\d+$', folder)]
        self.id = max(folder_numbers) if folder_numbers else 1
        
        self.recognizer = sr.Recognizer()

        self.audio_storage = []
        self.transcript_storage = []
        self.summary_storage = []
        self.question_storage = []

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

