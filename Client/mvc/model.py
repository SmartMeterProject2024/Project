# MVC - Model
class Model:
    def __init__(self):
        self.data = ""

    def set_data(self, data):
        # Add validation logic here
        self.data = data

    def get_data(self):
        return self.data