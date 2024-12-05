# Class definition for usage reading. Contain information needed for later processing.
class Reading:
    # Constructor for Reading class
    def __init__(self, time, usage):
        self.time = time
        self.usage = usage

    # Getter for time value
    def get_time(self):
        return self.time

    # Getter for reading usage value
    def get_usage(self):
        return self.usage