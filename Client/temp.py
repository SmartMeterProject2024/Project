import threading
import time
import socketio
import usage_generator
import json_converter
from mvc.controller import Controller
from mvc.usage_model import UsageModel
from mvc.view import View

socket = socketio.Client()
connected = False

@socket.event
def connect():
    global connected
    print("Connection established. (ID: " + socket.sid + ")")
    controller.update_server_status(True)
    connected = True

@socket.event
def connection_error(data):
    global connected
    print("Failed to connect to server.")
    print(data)
    controller.update_server_status(False)
    connected = False

@socket.event
def disconnect():
    global connected
    print("Disconnected from client")
    controller.update_server_status(False)
    connected = False

@socket.event
def Hello(data):
    global current_usage, bill
    print("Hello message received: " + data)

def start_generating_usage():
    # Update every interval
    usage_generator.start_generating_usage(handle_generated_usage)

def connect_to_server():
    print("Attempting to connect...")
    try:
        global connected
        socket.connect("http://localhost:3000")
        print("Connected")
        connected = True
    except socketio.exceptions.ConnectionError:
        print("Couldn't connect to Server. Retrying in 5 seconds...")
        controller.update_server_status(False)
        time.sleep(5)  # Wait for 5 seconds before retrying
        connect_to_server()

def start_connection_thread():
    connection_thread = threading.Thread(target=connect_to_server)
    connection_thread.start()

def handle_generated_usage(new_usage):
    global controller
    reading_to_send = controller.create_reading(new_usage)
    if connected:
        id = 123
        time = reading_to_send.get_time()
        current_usage = reading_to_send.get_usage()
        json_result = json_converter.convert_to_json(id, time, current_usage)
        print(f"Sending Reading: {current_usage} kWh")
        socket.emit('Send_Reading', json_result)

        # TODO: When server is set up, delete bill calculation
        cost_per_kwh = 0.08
        added_bill = (current_usage * cost_per_kwh)
        controller.update_bill(added_bill)

if __name__ == "__main__":
    global model, view, controller
    model = UsageModel(usage_generator.generate_usage(), 0.0, 0.00) # to update total and bill from mock
    view = View()
    controller = Controller(model, view)

    usage_thread = threading.Thread(target=start_generating_usage)
    usage_thread.daemon = True # allows the thread to exit when the main program does
    usage_thread.start()
    start_connection_thread()
    view.run()