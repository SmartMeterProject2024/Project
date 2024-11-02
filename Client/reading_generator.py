import random
import time

def start_generating_readings():
  while True:
    wait_for_next_interval()
    num = generate_reading()
    print(num)

def wait_for_next_interval():
   # start timer for next generated reading
    interval = random.randint(15, 60)
    time.sleep(interval)

def generate_reading():
  num = random.randint(0, 1000) # inclusive
  # 1 decimal place
  usage = (num if num == 0 else num / 10)
  return usage

if __name__ == '__main__':
    start_generating_readings()
