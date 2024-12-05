import random
import time

def handle_print_interval(interval): # Won't be triggered during tests
    print(f"(Next reading in {interval} seconds)")

# Start loop for generating client side readings
def start_generating_usage(callback):
    global interval
    while True:
        wait_for_next_interval(handle_print_interval)
        new_usage = generate_usage()
        callback(interval, new_usage)

def wait_for_next_interval(callback=None): # Sends interval to be printed
    global interval
    # start timer for next generated reading
    interval = random.randint(15, 60)
    if callback is not None:
        callback(interval)
    time.sleep(interval)

# Create a reading of a random value between 0.1 and 2 kw
def generate_usage():
    num = random.randint(0, 20) # inclusive
    usage = (num if num == 0 else num / 100) # 2 decimal place
    return float(usage)
