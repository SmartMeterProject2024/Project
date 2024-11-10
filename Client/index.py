import time
import socketio
import reading_generator
import json_converter as json
from datetime import datetime

socket = socketio.Client()

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
    # triggers 'handle_generated_reading' every interval in 'start_generating_readings()'
    reading_generator.start_generating_readings(handle_generated_reading)

def handle_generated_reading(usage):
    id = 123
    time = datetime.now().isoformat()
    json_result = json.convert_to_json(id, time, usage)
    print(f"Sending Reading: {usage} kWh")
    socket.emit('Send_Reading', json_result)

def connect_to_server():
    connected = False
    while not connected:
        try:
            socket.connect("http://localhost:3000")
            print("Connected")
            connected = True
        except socketio.exceptions.ConnectionError:
            print("Couldn't connect to Server. Retrying in 5 seconds...")
            time.sleep(5)

def main():
    connect_to_server()
    socket.wait()

if __name__ == '__main__':
    main()