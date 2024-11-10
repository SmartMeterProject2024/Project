import threading
import socketio
import reading_generator
import json_converter as json
from datetime import datetime
import ui as client_ui

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
    update_view(usage)

def connect_to_server():
    print("Attempting to connect...")
    try:
        socket.connect("http://localhost:3000")
        print("Connected")
    except socketio.exceptions.ConnectionError:
        print("Couldn't connect to Server. Retrying in 5 seconds...")
        view.after(5000, connect_to_server)

def start_connection_thread():
    connection_thread = threading.Thread(target=connect_to_server)
    connection_thread.start()

def main():
    global view, update_view
    # Start the UI
    view, update_view = client_ui.launch_ui()
    view.after(1500, start_connection_thread)  # Start connection attempt shortly after UI launch
    view.mainloop()
    

if __name__ == '__main__':
    main()