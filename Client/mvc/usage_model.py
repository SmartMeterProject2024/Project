# MVC - Model
class UsageModel:
    def __init__(self, current_usage, total_usage, bill):
      self.current_usage = current_usage
      self.total_usage = total_usage
      self.bill = bill

    def set_current_usage(self, data):
      self.current_usage = data

    def get_current_usage(self):
      return self.current_usage

    def set_total_usage(self, data):
      self.total_usage = data

    def get_total_usage(self):
      return self.total_usage

    def set_bill(self, data):
      self.bill = data

    def get_bill(self):
      return self.bill