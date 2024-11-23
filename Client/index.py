import threading
import socketio
import reading_generator
#import json_converter as json
import json
from datetime import datetime
import ui as client_ui
import random

# This is the number that identifies an end user. This is tied to the user's bill and account with the supplier.
# It would be static per user, and entered upon installation into the home.
id = random.getrandbits(32)
# This is a secret value tied to the hardware unit. It proves the traffic to the server is from a credible source.
# It would be static per device, assigned on hardware creation, not known by anyone other than the server upon pairing with user id
chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
secret = ''.join(random.choice(chars) for _ in range(64))


socket = socketio.Client()
connected = False
bill = 0  # Initial bill amount
current_usage = 2.1 # Initial usage

@socket.event
def connect():
    global id
    print("Connection established. (ID: " + socket.sid + ")")
    print("Attempting authentication with server...")
    data = {
        "id": id,
        "token": secret
    }
    socket.emit("authenticate", data, callback=authResponse)


@socket.on("responseEvent")
def authResponse(data):
    global connected
    if data == False: 
        print("Authentication unsuccessful")
    else: 
        print("Authenticated")
        connected = True
        update_server_status(True)
        # triggers 'handle_generated_reading' every interval in 'start_generating_readings()'
        reading_generator.start_generating_readings(handle_generated_reading)

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

def handle_generated_reading(usage):
    global bill, current_usage, id
    if connected:
        time = datetime.now().isoformat()
        data = {
            "id": id,
            "time": time,
            "usage": current_usage
        }
        print(f"Sending Reading: {current_usage} kWh")
        socket.emit('reading', data)
    current_usage = usage # prepare for next reading
    

@socket.event
def updateBill(data):
    global bill, current_usage
    bill = data
    update_view(current_usage, bill)

@socket.event
def warning(data):
    # DISPLAY WARNING MESSAGE TO CLIENT
    print("Warning received from server:")
    print(data)

def connect_to_server():
    print("Attempting to connect...")
    try:
        socket.connect("http://localhost:3000")
    except: # socketio.exceptions.ConnectionError:
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