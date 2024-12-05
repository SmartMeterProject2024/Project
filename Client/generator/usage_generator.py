import random
import time

from generator.subject import Subject

class UsageGenerator(Subject):
    def __init__(self):
        super().__init__() # implements Subject class

    # called once on client startup
    def start_generating_usage(self):
      while True:
            try:
                interval = self.wait_for_next_interval()
                new_usage = self.generate_usage()
                self.notify(interval, new_usage) # updates the controller listening
            except Exception as e:
                print(f"Failed to generate electricity usage: {e}")  

    def wait_for_next_interval(self):
        global interval
        # start timer for next generated reading
        interval = random.randint(15, 60)
        print(f"(Next reading in {interval} seconds)")
        time.sleep(interval) # waits until interval met
        return interval

    # Create a reading of a random value between 0.1 and 2 kw
    def generate_usage(self):
        num = random.randint(0, 200) # inclusive
        # to 2 decimal places
        usage = (num if num == 0 else num / 100)
        return float(usage)
