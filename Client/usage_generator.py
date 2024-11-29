import random
import time

def handle_print_interval(interval): # Won't be triggered during tests
   print(f"(Next reading in {interval} seconds)")

def start_generating_usage(callback):
  while True:
    wait_for_next_interval(handle_print_interval)
    num = generate_usage()
    callback(num)

def wait_for_next_interval(callback=None): # Sends interval to be printed
   # start timer for next generated reading
    interval = random.randint(15, 60)
    if callback is not None:
        callback(interval)
    time.sleep(interval)

def generate_usage():
  num = random.randint(0, 2500) # inclusive
  # 1 decimal place
  usage = (num if num == 0 else num / 100)
  return usage

if __name__ == '__main__':
    start_generating_usage()
