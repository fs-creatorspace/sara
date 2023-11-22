from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")

# Mock data for demonstration purposes
# Hey there! I was just thinking about achievements and accomplishments. So, what would you say is your proudest accomplishment?
## Oh, that's a tough one. I guess if I had to pick one, it would be completing a marathon. I remember It was both physically and mentally challenging, but the sense of achievement was incredible.
# Wow, that's impressive! I can imagine the dedication and training it must have taken. What motivated you to take on such a challenge?
## Well, I've always been into fitness and running a marathon was a bucket list goal for me. I wanted to prove to myself that I could push my limits and achieve something that seemed almost impossible at first.
# That's inspiring! It's amazing how setting and achieving personal goals can be so fulfilling. Have you always been someone who sets ambitious goals for yourself?
## I think so. Setting goals gives me a sense of direction and purpose. It's not always about the end result, but the journey and growth along the way.
interface_state = {'state': 'talk', 'text': "Hey there! I was just thinking about achievements and accomplishments. So, what would you say is your proudest accomplishment?"}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_interface_state', methods=['GET'])
def get_interface_state():
    return jsonify(interface_state)



@app.route('/test', methods=['GET'])
def test_route():
    return 'Test route is working!'


@socketio.on('interface_updated')
def handle_interface_update(data):
    interface_state['state'] = data['state']
    interface_state['text'] = data['text']
    emit('interface_updated', interface_state, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
