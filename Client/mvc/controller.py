# MVC - Controller
from datetime import datetime
from reading import Reading


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.update_view()

    def create_reading(self, new_usage):
        current_time = datetime.now().isoformat()
        current_usage = self.model.get_current_usage()
        # Send the displayed usage to the server
        new_reading = Reading(current_time, current_usage)
        # update the view with the new usage to be sent next call
        new_total_usage = self.model.get_total_usage() + current_usage
        self.model.set_current_usage(new_usage)
        self.model.set_total_usage(new_total_usage)
        self.update_view()
        return new_reading
    
    def update_bill(self, reading_cost):
        self.model.set_bill(self.model.get_bill() + reading_cost)
        self.update_view()

    def update_view(self):
        usage = self.model.get_current_usage()
        bill = self.model.get_bill()
        self.view.update_ui(usage, bill)

    def update_server_status(self, connected):
        self.view.update_server_connection(connected)

    def handle_submit(self):
        data = self.view.entry.get()
        self.model.set_data(data)
        self.view.show_message(f"You entered: {self.model.get_data()}")