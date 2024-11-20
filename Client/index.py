import threading
import socketio
import reading_generator
import json_converter as json
from datetime import datetime
import ui as client_ui

socket = socketio.Client()
connected = False
bill = 1.84  # Initial bill amount
current_usage = 2.1 # Initial usage

@socket.event
def connect():
    global connected
    print("Connection established. (ID: " + socket.sid + ")")
    update_server_status(True)
    connected = True

@socket.event
def connection_error(data):
    global connected
    print("Failed to connect to server.")
    print(data)
    update_server_status(False)
    connected = False

@socket.event
def disconnect():
    global connected
    print("Disconnected from client")
    update_server_status(False)
    connected = False

@socket.event
def Hello(data):
    global current_usage, bill
    print("Hello message received: " + data)
    # triggers 'handle_generated_reading' every interval in 'start_generating_readings()'
    reading_generator.start_generating_readings(handle_generated_reading)

def handle_generated_reading(usage):
    global bill, current_usage
    if connected:
        id = 123
        time = datetime.now().isoformat()
        json_result = json.convert_to_json(id, time, current_usage)
        print(f"Sending Reading: {current_usage} kWh")
        socket.emit('Send_Reading', json_result)

        # TODO: When server is set up, delete bill calculation
        cost_per_kwh = 0.08
        bill += (current_usage * cost_per_kwh)
    update_view(usage, bill)
    current_usage = usage # prepare for next reading

def connect_to_server():
    print("Attempting to connect...")
    try:
        global connected
        socket.connect("http://localhost:3000")
        print("Connected")
        connected = True
    except socketio.exceptions.ConnectionError:
        print("Couldn't connect to Server. Retrying in 5 seconds...")
        update_server_status(False)
        view.after(5000, connect_to_server)

def start_connection_thread():
    connection_thread = threading.Thread(target=connect_to_server)
    connection_thread.start()

def main():
    global view, update_view, update_server_status
    # Start the UI
    view, update_view, update_server_status = client_ui.launch_ui()
    current_usage = reading_generator.generate_usage()
    # TODO: When mocking is complete, replace bill
    update_view(current_usage, bill) # initial values
    view.after(1500, start_connection_thread)  # Start connection attempt shortly after UI launch
    view.mainloop()
    

if __name__ == '__main__':
    main()