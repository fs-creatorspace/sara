import openai
import speech_recognition as sr
import gtts
from dotenv import load_dotenv
import pygame.mixer
import os
import re

def Conversation():
    def __init__(self, path: str, name, age):

        # Getting List of all folders
        folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        # Extract the numbers at the end of the folder names, convert them to integers, and find the maximum
        folder_numbers = [int(re.search(r'\d+$', folder).group()) for folder in folders if re.search(r'\d+$', folder)]
        self.id = max(folder_numbers) if folder_numbers else 1
        self.name = name
        self.age = age

