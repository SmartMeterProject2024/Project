import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.widgets import Meter
from random import randint

# Fonts
font_reg = ("Verdana", 14, "normal")
font_small = ("Verdana", 10, "normal")
font_bold = ("Verdana", 16, "bold")
font_heading = ("Verdana", 20, "bold")

# Create the main window with ttkbootstrap
root = ttk.Window(themename="darkly")
root.title("Smart Meter UI")
root.geometry("400x300")
root.minsize(400, 300)

# Variables to store the target usage level and step size
target_usage = 50
current_usage = 50

# Function to smoothly update the gauge towards the target usage level
def smooth_update():
    global current_usage
    # If the current usage is not equal to the target, move towards it
    if current_usage < target_usage:
        current_usage += 1  # Increment for increase
    elif current_usage > target_usage:
        current_usage -= 1  # Decrement for decrease
    else:
        return  # Exit if target is reached

    # Update the meter display
    meter.amountused = current_usage
    lblUsageVal.config(text=f"{current_usage} kWh")

    # Adjust color based on usage level
    if current_usage < 33:
        meter.configure(bootstyle="success")
    elif current_usage < 66:
        meter.configure(bootstyle="warning")
    else:
        meter.configure(bootstyle="danger")

    # Continue updating every 50 milliseconds
    root.after(50, smooth_update)

# Function to set a new random target usage level
def update_gauge():
    global target_usage
    target_usage = randint(0, 100)  # Set a new random target
    smooth_update()  # Begin the smooth transition

# Heading label
lblHeading = ttk.Label(root, text="Smart Meter", font=font_heading, anchor='center')
lblHeading.grid(row=0, column=0, columnspan=3, pady=(10, 0))

# Create and place the Meter (gauge) widget
meter = Meter(
    root,
    metersize=180,
    amountused=current_usage,  # Start at initial usage level
    metertype='semi',
    subtext="Energy Usage",
    interactive=False,
    bootstyle="success"
)
meter.grid(row=1, column=0, columnspan=3, pady=(10, 0))

# Current budget and time display
lblBudget = ttk.Label(root, text="Budget", font=font_small)
lblBudget.grid(row=2, column=0, columnspan=3)

lblTime = ttk.Label(root, text="14:38", font=font_bold)
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

# Run the application
root.mainloop()
