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

print(get_answer())