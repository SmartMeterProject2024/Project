import sys
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.widgets import Meter
from random import randint
from datetime import datetime

# Fonts
font_reg = ("Verdana", 14, "normal")
font_small = ("Verdana", 10, "normal")
font_bold = ("Verdana", 16, "bold")
font_heading = ("Verdana", 20, "bold")

# variables
target_usage = 50
current_usage = 50

# recurring ui components
root = None
meter = None
lblUsageVal = None
lblTime = None

def launch_ui():
    global root, meter, current_usage, target_usage, lblUsageVal, lblTime
    # Create the main window with ttkbootstrap
    root = ttk.Window(themename="darkly")
    root.title("Smart Meter UI")
    root.geometry("800x600")
    root.minsize(800, 600)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Heading label
    lblHeading = ttk.Label(root, text="Smart Meter", font=font_heading, anchor='center')
    lblHeading.grid(row=0, column=0, columnspan=3, pady=(10, 0))

    # Create and place the Meter (gauge) widget
    meter = Meter(
        root,
        metersize=180,
        amountused=current_usage,
        metertype='semi',
        subtext="Energy Usage",
        interactive=False,
        bootstyle="success"
    )
    meter.grid(row=1, column=0, columnspan=3, pady=(10, 0))

    # Current budget and time display
    lblBudget = ttk.Label(root, text="Budget", font=font_small)
    lblBudget.grid(row=2, column=0, columnspan=3)

    lblTime = ttk.Label(root, text=datetime.now().strftime("%H:%M"), font=font_bold)
    lblTime.grid(row=1, column=2, sticky='e')

    # Energy usage and bill labels
    lblUsage = ttk.Label(root, text="Energy Usage", font=font_bold)
    lblUsage.grid(row=3, column=0)
    lblUsageVal = ttk.Label(root, text=f"{current_usage} kWh", font=font_reg)
    lblUsageVal.grid(row=4, column=0)

    lblBill = ttk.Label(root, text="Bill", font=font_bold)
    lblBill.grid(row=3, column=2)
    lblBillVal = ttk.Label(root, text="£6.84", font=font_reg)
    lblBillVal.grid(row=4, column=2)

    # Button to update gauge randomly
    btnRandomUsage = ttk.Button(root, text="Randomize Usage", bootstyle="outline-light", command=update_gauge)
    btnRandomUsage.grid(row=5, column=0, columnspan=3, pady=20)

    # Configure grid to expand
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

    update_time()
    return root

def update_ui():
    root.after(5000, update_ui)


# Function to smoothly update the gauge towards the target usage level
def smooth_update():
    global current_usage
    # Smoothly approach the target usage
    if current_usage < target_usage:
        current_usage += 3 if (target_usage - current_usage > 10) else 1  # Increment to increase
    elif current_usage > target_usage:
        current_usage -= 3 if (current_usage - target_usage > 10) else 1  # Decrement to decrease

    # Update the meter display and subtext
    meter.configure(amountused=current_usage, subtext=f"{current_usage} kWh")
    lblUsageVal.config(text=f"{current_usage} kWh")

    # Change color based on usage level
    if current_usage < 33:
        meter.configure(bootstyle="success")
    elif current_usage < 66:
        meter.configure(bootstyle="warning")
    else:
        meter.configure(bootstyle="danger")

    # Continue updating until reaching the target
    if current_usage != target_usage:
        root.after(20, smooth_update)  # Recursive call

# Function to set a new random target usage level
def update_gauge():
    global target_usage
    target_usage = randint(0, 100)  # Set a new random target
    smooth_update()  # Begin smooth transition

def update_time():
    lblTime.config(text=datetime.now().strftime("%H:%M"))
    lblTime.after(5000, update_time)

def on_closing():
    print("Shutdown")
    sys.exit()
