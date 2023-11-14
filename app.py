from conversation import Conversation
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socket = SocketIO(app)
conv = Conversation("conversations")

@app.route('/')
def index():
    return render_template('index.html')

@socket.on('message')
def handle_message(data):
    print("Client says: ", data)

@socket.on('connect')
def handle_connect():
    print('Client connected -> Running conversation')

    conv = Conversation("conversations")

    # Generate the first question audio
    question_path = conv.textToSpeech(conv.question_storage[-1])

    # Write the first question audio to the interface
    socket.emit("emotion", "speak")
    socket.emit('text', conv.question_storage[-1])

@socket.on('speak')
def handle_speak():

    # Get question path
    question_path = conv.textToSpeech(conv.question_storage[-1])

    # Speak question out loud
    conv.speak(question_path)

    socket.emit("emotion", "listen")
    socket.emit("text", "I am listening")

@socket.on("listen")
def handle_listen():
    # Listen to the answer
    answer_audio = conv.record()

    socket.emit("emotion", "think")
    socket.emit("text", "I am thinking")

@socket.on("think")
def handle_think():

    answer_text = conv.speechToText()
    
    # Summarize answer
    conv.summarize(answer_text)

    # Generate a follow up question
    follow_up_question = conv.generateQuestion()

    # Show the histiry for debug reasons
    conv.showHistory()

    # Increase conversation counter by one so files don't get overridden
    conv.conv_counter += 1

    # Generate audio for next question
    question_path = conv.textToSpeech(follow_up_question)

    socket.emit("emotion", "speak")
    socket.emit("text", follow_up_question)

if __name__ == '__main__':
    app.run(debug=True)