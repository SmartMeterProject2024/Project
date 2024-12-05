# Modules needed in the program
import threading
import time
import socketio
import random
# Bring in code to generate realistic energy usage
from generator.usage_generator import UsageGenerator

# Bring in logic for MVC model
from mvc.usage_controller import UsageController
from mvc.usage_model import UsageModel
from mvc.usage_view import UsageView

# This is the number that identifies an end user. This is tied to the user's bill and account with the supplier.
# It would be static per user, and entered upon installation into the home.
id = random.getrandbits(32)
# This is a secret value tied to the hardware unit. It proves the traffic to the server is from a credible source.
# It would be static per device, assigned on hardware creation, not known by anyone other than the server upon pairing with user id
chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
secret = ''.join(random.choice(chars) for _ in range(64))

# Initialising variables for use throughout program
socket = socketio.Client()
connected = False


# Listen for connect event. Fires when a successful websocket connection is made
@socket.event
def connect(): # Triggered on new connection with Server
    global id
    print("Connected to server. (ID: " + socket.sid + ")")
    print("Attempting authentication with server...")
    data = {
        "id": id,
        "token": secret
    }
    # Attempt to authenticate with client. Response handled by authResponse function
    socket.emit("authenticate", data, callback=authResponse)

# Callback function for authentication
@socket.on("responseEvent")
def authResponse(data): # Triggered after authentication attempt
    global connected
    if data == False: 
        print("Authentication unsuccessful")
        connected = False
        controller.update_server_status(False) # update server icon in view
    else: 
        print("Authenticated")
        connected = True
        controller.update_server_status(True)
        socket.emit("check_grid_status", callback=receive_grid_status) # checks grid status

@socket.on("responseEvent")
def receive_grid_status(is_errored): # Triggered when grid status updates
    controller.update_grid_status(not is_errored)

# Output to console when connection error occurs, retry connection
@socket.event
def connection_error(data): # Triggered when connection to server errors
    global connected
    print("Failed to connect to server.")
    print(data)
    controller.update_server_status(False)
    connected = False

# Output to console when client disconnects from server. Attempt to reconnect.
@socket.event
def disconnect(): # Triggered when disconnected from Server
    global connected
    print("Disconnected from Server")
    controller.update_server_status(False)
    connected = False
    controller.update_grid_status(False)

# Called by controller when notified of a new reading
# Given an energy usage, generate a reading, send to server, and log to console.
def handle_generated_usage(interval, new_usage):
    global id, controller, connected
    try:
        controller.update_usage_stats(interval, new_usage) # updates model
        reading_to_send = controller.create_reading()
        controller.update_usage_display() # updates view
        if connected:
            # a Python dictionary automatically converts into a JSON object
            # which is sent to the server so no need for a JSON formatter
            data = {
                "id": id,
                "time": reading_to_send.get_time(),
                "usage": reading_to_send.get_usage()
            }
            print(f"Sending Reading: {reading_to_send.get_usage()} kWh")
            socket.emit('reading', data) # send reading to server
    except RuntimeError as e:
        print(f"Couldn't create Reading: {e}")
    except Exception as ex:
        print(f"Something went wrong: {ex}")
    
# Force display an updated bill from the server
@socket.event
def updateBill(data):
    controller.update_bill(data)

# Force displat an updated total usage from the server
@socket.event
def updateUsage(data):
    controller.update_total_usage(data)
    controller.update_view()

# Take warning messages from server and display them
@socket.event
def warning(message):
    global controller
    # DISPLAY WARNING MESSAGE TO CLIENT
    print("Warning received from server: " + message)
    controller.update_grid_status(False, message)
    
@socket.event
def resolved():
    print("Warning resolution received from server")
    controller.update_grid_status(True)


# Set up a connection to the server. On failure, wait 5 seconds and retry
def connect_to_server():
    print("Attempting to connect...")
    try:
        socket.connect("http://localhost:3000")
    except: 
        print("Couldn't connect to Server. Retrying in 5 seconds...")
        controller.update_server_status(False)
        time.sleep(5)
        connect_to_server()

# Start up a connection in a new thread so as not to interrupt the rest of the program
def start_connection_thread():
    try:
        connection_thread = threading.Thread(target=connect_to_server)
        connection_thread.daemon = True # allows the thread to exit when the main program does
        connection_thread.start()
    except Exception as e:
        print(f"Failed to start connection thread: {e}")

def start_usage_generator_thread(generator): 
    try:
        usage_thread = threading.Thread(target=generator.start_generating_usage)
        usage_thread.daemon = True # allows the thread to exit when the main program does
        usage_thread.start()
    except Exception as e:
        print(f"Failed to start usage generator thread: {e}")

# Start up a generator for energy readings in a new thread so as not to interrupt the rest of the program
if __name__ == "__main__":
    global model, view, controller
    try:
        usage_generator = UsageGenerator()
        model = UsageModel(usage_generator.generate_usage(), 0.0, 0.00) # to update total and bill from mock
        view = UsageView()
        controller = UsageController(model, view, handle_generated_usage)
        usage_generator.attach(controller)
        start_usage_generator_thread(usage_generator)
        start_connection_thread()
        view.run()
    except Exception as e:
        print(f"Failed to start client: {e}")