import gtts

def save_question(question, audio_id):

    # Convert text to speech
    tts = gtts.gTTS(text=question, lang='en')
    path = f"./questions/question_{audio_id}.mp3"
    tts.save(path)
    
    return path


import os
import pygame

def play_question(path):
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

import speech_recognition as sr
def get_answer():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please speak something...")
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        audio_data = recognizer.listen(source)
        print("Recognizing...")

        try:
            
            # Get WAV data from captured audio
            wav_data = audio_data.get_wav_data()
            
            # Using Google's speech recognition
            text = recognizer.recognize_google(audio_data)
            print(f"You said: {text}")
            

        except sr.UnknownValueError:
            text = "UnknownValueError"   #REMOVE THIS LATER!!!!!!!!!!!!
            print("I not understand the audio.")
        except sr.RequestError:
            print("API Error.")
    
    return text


import openai
# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text):
    messages = [
        {"role": "system", "content": "You are a helpful assistant focussing on receiving a good story."},
        {"role": "user", "content": f"Provide a brief summary of the following text and correct any grammar mistakes/wrong words. Dont change the meaning of the text.: '{text}'"}
    ]
    
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    
    return response.choices[0].message['content'].strip()


import openai
def ask_follow_up_q(questions: str, summary: str):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that asks questions relevant to a story."},
        {"role": "user", "content": f"You are given a summary of a previously asked questions. Ask a relevant follow up Question (that has not been asked before) to get more relevant information about the summary. Use simple Vocabulary and talk like you are in a real conversation: Questions: '{questions}' Summary:'{summary}'"}
    ]
    
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    
    return response.choices[0].message['content'].strip()