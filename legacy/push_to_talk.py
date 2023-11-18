import speech_recognition as sr

def push_to_talk():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    print("Recording... Press Enter to stop recording.")

    recording = True  # Start recording automatically

    while recording:
        with microphone as source:
            audio = recognizer.listen(source)

        print("Processing...")
        try:
            text = recognizer.recognize_google(audio)
            print(f"Google Speech Recognition: {text}")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

        # Wait for user input (Enter key press)
        input_state = input()

        if input_state == "":
            recording = False  # Stop recording on Enter press

if __name__ == "__main__":
    push_to_talk()
