from conversation import *

conv = Conversation("conversations")

# Set the first question
question_path = conv.textToSpeech(conv.question_storage[-1])

while True:
    # Speak question out loud
    conv.speak(question_path)

    # Listen to the answer
    answer_audio = conv.record()

    # Convert answer to text
    answer_text = conv.speechToText(answer_audio)

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