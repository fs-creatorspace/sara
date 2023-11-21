from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
<<<<<<< Updated upstream
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")

# Mock data for demonstration purposes
interface_state = {'state': 'talk', 'text': "Some Txt herrre??"}
=======
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:8080"}})

socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:8080")

# Mock data for demonstration purposes
interface_state = {'state': 'talk', 'text': "Dit is een test neef "}
>>>>>>> Stashed changes


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
