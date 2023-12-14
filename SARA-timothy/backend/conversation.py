import openai
import speech_recognition as sr
import gtts
from dotenv import load_dotenv
import pygame.mixer
import os
import random

class Conversation():
    def __init__(self, path: str, load = 0, question_limit = 3):
        
        self.path = path
        self.conv_counter = 0
        self.recognizer = sr.Recognizer()
        self.question_limit = question_limit
        
        self.question_storage = []
        self.audio_storage = []
        self.transcript_storage = []
        self.summary_storage = []

        starting_questions = [  "Hey! I was just thinking about memories. Do you have any childhood memory that makes you feel especially nostalgic?",
                                "Hey there! I was just thinking about achievements and accomplishments. So, what would you say is your proudest accomplishment?",
                                "Hey! I was just reminiscing about some funny moments in life. Do you have a memory that always makes you laugh when you think about it? What's your funniest memory?"
                            ]
        if load:
            self.id = load
            # TBD
            # Load all data from folder
        else:
            # TBD
            # Load random start question
            self.question_storage.append(random.choice(starting_questions))
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
        # Saves wav as a new file in conversation folder and sr.AudioData-object in audio_storage)
        
        with sr.Microphone() as source:
            print("Please speak something...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            self.recognizer.energy_threshold = 4000
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
        
        self.audio_storage.append(audio_data)
        
        return audio_data
    
    
    def speechToText(self, audioData: sr.AudioData = None, bypass = "") -> str:
        # Recieves audio data object and returns a transcript
        # Saves transcript to transcript_storage

        if bypass:
            text = bypass
        else:
            if audioData:
                text = self.recognizer.recognize_google(audioData)
            else:
                audioData = self.audio_storage[-1]
                try:
                    text = self.recognizer.recognize_google(audioData)
                except sr.UnknownValueError:
                    text = "Sorry, I couldn't understand the audio."
        print(f"You said: {text}")
        self.transcript_storage.append(text)
        return text
    
    def summarize(self, text: str) -> str:
        # Recieves raw text, refines grammar and summarizes it
        # Saves summary to summary_storage
        messages = [
        {"role": "system", "content": "You are a helpful assistant focussing on receiving a good story."},
        {"role": "user", "content": f"Provide a brief summary of the following text and correct any grammar mistakes/wrong words. Dont change the meaning of the text. If you dont find any mistakes, return the original text instead: '{text}'"}
        ]
    
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

        summary_q = response.choices[0].message['content'].strip()
        self.summary_storage.append(summary_q)
        return summary_q
    
    def generateQuestion(self) -> str:
        # Takes all summaries and all questions and generates a new question with use of LLM
        # Saves new question to question_storage

        if len(self.question_storage) >= self.question_limit:
            output = ""
            for index, question in enumerate(self.question_storage):
                output += f"question {index}:<br>{question}<br><br>answer {index}:<br>{self.transcript_storage[index]}<br><br>"
            self.question_storage.append(output)
            return output

        messages = [
        {"role": "system", "content": "You are a helpful assistant that asks questions relevant to a story. Address the user like you are talking to them when asking questions"},
        #{"role": "user", "content": f"You are given a summary of a previously asked questions. Ask a relevant follow up Question (that has not been asked before) to get more relevant information about the summary. Use simple Vocabulary and talk like you are in a real conversation: Questions: '{self.question_storage}' Summary:'{self.summary_storage}'"}
        #new template Try:
        {"role": "user","content": f"You are given a summary of a previously asked question. Ask a relevant follow-up question (that has not been asked before) to get more relevant information about the summary. Use simple vocabulary and talk like you are in a real conversation.\n\nQuestions: {', '.join(self.question_storage)}\n\nSummary: {self.summary_storage}"}
        ]
    
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

        follow_up_q = response.choices[0].message['content'].strip()
        self.question_storage.append(follow_up_q)
        return follow_up_q

    def showHistory(self) -> str:
        # prints out the question_storage and summary_storage
        print("Questions:")
        for idx, q in enumerate(self.question_storage):
            print(f"{idx}: {q}")
        
        print("----------")
        print("Summaries:")
        for idx, s in enumerate(self.summary_storage):
            print(f"{idx}: {s}")

        return

    def summary(self) -> str:
        #creates a summary of all questions/answer pairs
        # Form a dialogue from the provided lists
        dialogue = []
        for question, answer in zip(self.question_storage, self.summary_storage):
            dialogue.append({"role": "user", "content": question})
            dialogue.append({"role": "assistant", "content": answer})

        # Generate a story summary using ChatGPT
        messages = [
            {"role": "system", "content": "You are a storyteller summarizing story based on questions and answers."},
            *dialogue,
            {"role": "user", "content": "Summarize the story. Address the user directly as if you would tell them the story in person."}
        ]

        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        summary = response.choices[0].message['content'].strip()

        return summary