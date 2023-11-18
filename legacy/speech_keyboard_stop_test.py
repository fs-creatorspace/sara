import keyboard
import speech_recognition as sr
import threading

# Create a recognizer and microphone instance
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# This variable will be used to control the recording thread
recording = threading.Event()
recording.set()  # Start recording

def record():
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        while recording.is_set():
            print("Recording...")
            try:
                audio = recognizer.listen(source, timeout=5)  # Set timeout to 5 seconds
                print("Processing...")
                text = recognizer.recognize_google(audio)
                print(f"Google Speech Recognition: {text}")
            except sr.WaitTimeoutError:
                continue  # If no speech is detected within the timeout, continue recording
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

# Start the recording thread
threading.Thread(target=record).start()

# Wait for 'a' key press to stop recording
keyboard.wait('a')
recording.clear()

print("Recording stopped.")