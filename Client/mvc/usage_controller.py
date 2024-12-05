# MVC - Controller
from datetime import datetime
from generator.observer import Observer
from reading import Reading

class UsageController(Observer): # implements Observer class
    def __init__(self, model, view, event_handler):
        self.model = model
        self.view = view
        self.event_handler = event_handler # used to callback to index
        self.update_view() # loads initial view
        self.last_total_usage = model.get_total_usage() # used later to calculate change in usage

    # triggered by usage_generator creating a new reading
    def update(self, interval, usage):
        self.event_handler(interval, usage)

    # called by index
    def update_usage_display(self):
        self.update_view()

    # updates usage model
    def update_usage_stats(self, seconds_since_last, new_usage):
        # converting from current usage kW to total usage kWh, accounting for time spent on current usage
        # new_total_usage = self.model.get_total_usage() + (self.model.get_current_usage() * (seconds_since_last / 3600.0))
        # for the sake of the demo, we'll treat 1 second as 1 minute so total usage is visible
        try:
            print("total usage before: " + str(self.model.get_total_usage()) + " kWh")
            new_total_usage = self.model.get_total_usage() + (self.model.get_current_usage() * (seconds_since_last / 60.0))
            self.model.set_current_usage(new_usage)
            self.last_total_usage = self.model.get_total_usage()
            self.model.set_total_usage(new_total_usage)
            print("total usage after: " + str(self.model.get_total_usage()) + " kWh")
        except Exception as e:
            raise RuntimeError(f"Error updating usage display: {e}")

    # returns a reading to index to send to server
    def create_reading(self):
        current_time = datetime.now().isoformat()
        converted_usage = self.model.get_total_usage() - self.last_total_usage
        # Send the displayed usage to the server
        new_reading = Reading(current_time, converted_usage)
        return new_reading
    
    # updates bill label in view
    def update_bill(self, new_total_bill):
        self.model.set_bill(new_total_bill)
        self.update_view()

    # updates total usage label in view
    def update_total_usage(self, new_total_usage):
        self.model.set_total_usage(new_total_usage)
        self.update_view()

    # full update of the view
    def update_view(self):
        current_usage = self.model.get_current_usage()
        total_usage = self.model.get_total_usage()
        bill = self.model.get_bill()
        try:
            self.view.update_ui(current_usage, total_usage, bill)
        except Exception as e:
            print(f"Error updating usage display: {e}")

    # updates server status in view
    def update_server_status(self, connected):
        try:
            self.view.update_server_connection(connected)
        except Exception as e:
            print(f"Failed to update server status icon: {e}")

    # updates grid status in view
    def update_grid_status(self, connected, message=""):
        try:
            self.view.update_grid_connection(connected, "Issue with grid detected - " + message)
        except Exception as e:
            print(f"Failed to update grid status display: {e}")