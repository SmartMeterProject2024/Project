import socketio
import json
from datetime import datetime

socket = socketio.Client()

def convert_to_json(id, time, usage):
    # Create a dictionary
    data = {
        "id": id,
        "time": time,
        "usage": usage
    }
    # Convert the dictionary to a JSON string
    json_object = json.dumps(data, indent=4)
    # Convert the json string to JSON object
    json_object = json.loads(json_object)
    return json_object

@socket.event
def connect():
    print("Connection established. (ID: " + socket.sid + ")")

@socket.event
def connection_error(data):
    print("Failed to connect to server.")
    print(data)

@socket.event
def disconnect():
    print("Disconnected from client")

@socket.event
def Hello(data):
    print("Hello message received: " + data)
    id = 123
    time = datetime.now().isoformat()
    usage = 45.67
    json_result = convert_to_json(id, time, usage)
    print(json_result)
    socket.emit('Hello World!', json_result)

socket.connect("http://localhost:3000")
socket.wait()