import random
import time

from generator.subject import Subject

class UsageGenerator(Subject):
  def __init__(self):
    super().__init__()

  def start_generating_usage(self):
    while True:
      try:
        interval = self.wait_for_next_interval()
        new_usage = self.generate_usage()
        self.notify(interval, new_usage)
      except Exception as e:
        print(f"Failed to generate electricity usage: {e}")  

  def wait_for_next_interval(self):
      global interval
    # start timer for next generated reading
      interval = random.randint(15, 60)
      print(f"(Next reading in {interval} seconds)")
      time.sleep(interval)
      return interval

  def generate_usage(self):
    num = random.randint(0, 2500) # inclusive
    # 2 decimal place
    usage = (num if num == 0 else num / 100)
    return float(usage)
