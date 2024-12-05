# MVC - Controller
from datetime import datetime
from reading import Reading

# Following MVC model, this class controls business logic behind the reading objects.
class UsageController:
    # Constructor for UsageController object
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.update_view()
        self.last_total_usage = model.get_total_usage()

    def update_usage_display(self):
        self.update_view()

    def update_usage_stats(self, seconds_since_last, new_usage):
        # converting from current usage kW to total usage kWh, accounting for time spent on current usage
        # new_total_usage = self.model.get_total_usage() + (self.model.get_current_usage() * (seconds_since_last / 3600.0))
        # for the sake of the demo, we'll treat 1 second as 1 minute so total usage is visible
        print("total usage before: " + str(self.model.get_total_usage()) + " kWh")
        new_total_usage = self.model.get_total_usage() + (self.model.get_current_usage() * (seconds_since_last / 60.0))
        self.model.set_current_usage(new_usage)
        self.last_total_usage = self.model.get_total_usage()
        self.model.set_total_usage(new_total_usage)
        print("total usage after: " + str(self.model.get_total_usage()) + " kWh")

    # Generates a usage reading from current time, current energy draw (sourced in Model)
    #  and updates view with new details
    def create_reading(self):
        current_time = datetime.now().isoformat()
        converted_usage = self.model.get_total_usage() - self.last_total_usage
        # Send the displayed usage to the server
        new_reading = Reading(current_time, converted_usage)
        return new_reading
    
    # Sets new bill value, ready to send to the view
    def update_bill(self, newTotalBill):
        self.model.set_bill(newTotalBill)
        self.update_view()

    # Displays up to date usage and bill values in the view
    def update_view(self):
        current_usage = self.model.get_current_usage()
        total_usage = self.model.get_total_usage()
        bill = self.model.get_bill()
        self.view.update_ui(current_usage, total_usage, bill)

    # Sends updated connection status to view
    def update_server_status(self, connected):
        self.view.update_server_connection(connected)
    
    def update_grid_status(self, connected, message=""):
        self.view.update_grid_connection(connected, "Issue with grid detected - " + message)