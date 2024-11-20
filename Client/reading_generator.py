import random
import time

def handle_print_interval(interval): # Won't be triggered during tests
   print(f"(Next reading in {interval} seconds)")

def start_generating_readings(callback):
  while True:
    wait_for_next_interval(handle_print_interval)
    num = generate_usage()
    callback(num)

def wait_for_next_interval(callback=None): # Implementation - callback | Test - none
   # start timer for next generated reading
    interval = random.randint(15, 60)
    if callback is not None:
        callback(interval)
    time.sleep(interval)

def generate_usage():
  num = random.randint(0, 250) # inclusive
  # 1 decimal place
  usage = (num if num == 0 else num / 10)
  return usage

if __name__ == '__main__':
    start_generating_readings()
