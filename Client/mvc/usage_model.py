# MVC - Model
class UsageModel:
    def __init__(self):
        self.current_usage = 0
        self.total_usage = 0
        self.bill = 0.00
        
    # Constructor for UsageModel class
    def __init__(self, current_usage, total_usage, bill):
        self.current_usage = current_usage
        self.total_usage = total_usage
        self.bill = bill

    # Setter for current_usage
    def set_current_usage(self, data):
        self.current_usage = data

    # Getter for current_usage
    def get_current_usage(self):
        return self.current_usage

    # Setter for total_usage
    def set_total_usage(self, data):
        self.total_usage = data

    # Getter for total_usage
    def get_total_usage(self):
        return self.total_usage

    # Setter for bill
    def set_bill(self, data):
        self.bill = data

    # Getter for bill
    def get_bill(self):
        return self.bill