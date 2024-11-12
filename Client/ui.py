import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.widgets import Meter
from random import randint, choice
from datetime import datetime
from tkinter import messagebox
import logging

# Set up logging configuration
logging.basicConfig(filename="error_log.txt", level=logging.ERROR,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Fonts
font_reg = ("Verdana", 14, "normal")
font_small = ("Verdana", 10, "normal")
font_bold = ("Verdana", 16, "bold")
font_heading = ("Verdana", 20, "bold")

# Create the main window with ttkbootstrap
root = ttk.Window(themename="darkly")
root.title("Smart Meter UI")
root.geometry("400x350")
root.minsize(400, 350)

# Variables to store usage, target usage, and bill
target_usage = 100
current_usage = 50
bill = 6.84  # Initial bill amount
cost_per_kwh = 0.14  # Cost per kWh

# Function to smoothly update the gauge towards the target usage level
def smooth_update():
    global current_usage
    if current_usage < target_usage:
        current_usage += 1
    elif current_usage > target_usage:
        current_usage -= 1

    meter.configure(amountused=current_usage, subtext=f"{current_usage} kWh")
    lblUsageVal.config(text=f"{current_usage} kWh")

    if current_usage < 33:
        meter.configure(bootstyle="success")
    elif current_usage < 66:
        meter.configure(bootstyle="warning")
    else:
        meter.configure(bootstyle="danger")

    if current_usage != target_usage:
        root.after(20, smooth_update)

# Function to set a new random target usage level
def update_gauge():
    global target_usage
    target_usage = randint(0, 100)
    smooth_update()

# Function to update the date and time displays
def update_time():
    lblTime.config(text=datetime.now().strftime("%H:%M"))
    lblDate.config(text=datetime.now().strftime("%Y-%m-%d"))
    lblTime.after(5000, update_time)

# Function to update the bill based on usage
def auto_update_bill():
    global bill, current_usage
    bill += current_usage * cost_per_kwh / 100  # Increment bill based on usage
    lblBillVal.config(text=f"£{round(bill, 2)}")
    root.after(5000, auto_update_bill)  # Schedule the next bill update in 5 seconds

# Function to simulate server communication
def check_server_connection():
    global connection_status
    connection_success = choice([True, False])  # Simulate connection status
    if connection_success:
        connection_status = "strong"
        signal_status.config(text="✔️")
        lblConnectionError.config(text="")
    else:
        connection_status = "lost"
        signal_status.config(text="❌")
        lblConnectionError.config(text="Communication error with server", bootstyle="danger")
        logging.error("Communication error with server")  # Log error message
    
    root.after(10000, check_server_connection)

# Function to simulate grid status check
def check_grid_status():
    global grid_status
    grid_issue = choice([True, False])  # Simulate grid status
    if grid_issue:
        grid_status = "issue"
        alert_status.config(text="❌")
        lblGridError.config(text="Electricity grid issue detected", bootstyle="danger")
        logging.error("Electricity grid issue detected")  # Log grid issue
    else:
        grid_status = "no_issue"
        alert_status.config(text="✔️")
        lblGridError.config(text="")
    
    root.after(15000, check_grid_status)

# Function to show connection status on click
def show_connection_status():
    status_message = "Connection strong" if connection_status == "strong" else "Connection lost"
    messagebox.showinfo("Connection Status", status_message)

# Function to show grid status on click
def show_grid_status():
    grid_message = "Electricity grid is stable" if grid_status == "no_issue" else "Electricity grid issue detected"
    messagebox.showinfo("Grid Status", grid_message)

# Date label in the top-left
lblDate = ttk.Label(root, text=datetime.now().strftime("%Y-%m-%d"), font=font_bold)
lblDate.grid(row=0, column=0, sticky='w', padx=10)

# Time label in the top-right
lblTime = ttk.Label(root, text=datetime.now().strftime("%H:%M"), font=font_bold)
lblTime.grid(row=0, column=2, sticky='e', padx=10)

# Heading label
lblHeading = ttk.Label(root, text="Smart Meter", font=font_heading, anchor='center')
lblHeading.grid(row=1, column=0, columnspan=3, pady=(10, 0))

# Separate error message labels for connection and grid issues
lblConnectionError = ttk.Label(root, text="", font=font_small, bootstyle="danger")
lblConnectionError.grid(row=2, column=0, columnspan=3, pady=(5, 0))

lblGridError = ttk.Label(root, text="", font=font_small, bootstyle="danger")
lblGridError.grid(row=3, column=0, columnspan=3, pady=(5, 0))

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
meter.grid(row=4, column=0, columnspan=3, pady=(10, 0))

# Current budget label
lblBudget = ttk.Label(root, text="Budget", font=font_small)
lblBudget.grid(row=5, column=0, columnspan=3)

# Energy usage and bill labels
lblUsage = ttk.Label(root, text="Energy Usage", font=font_bold)
lblUsage.grid(row=6, column=0)
lblUsageVal = ttk.Label(root, text=f"{current_usage} kWh", font=font_reg)
lblUsageVal.grid(row=7, column=0)

lblBill = ttk.Label(root, text="Bill", font=font_bold)
lblBill.grid(row=6, column=2)
lblBillVal = ttk.Label(root, text=f"£{bill}", font=font_reg)
lblBillVal.grid(row=7, column=2)

# Button to update gauge randomly
btnRandomUsage = ttk.Button(root, text="Randomise Usage", bootstyle="outline-light", command=update_gauge)
btnRandomUsage.grid(row=8, column=0, columnspan=3, pady=20)

# Signal icon and status (bottom-right) for connection
signal_frame = ttk.Frame(root)
signal_frame.grid(row=9, column=2, sticky='e', pady=10, padx=10)
signal_icon = ttk.Label(signal_frame, text="📶", font=font_bold, cursor="hand2")
signal_icon.pack(side="left")
signal_status = ttk.Label(signal_frame, text="✔️", font=font_bold, cursor="hand2", width=2)
signal_status.pack(side="left")
signal_status.bind("<Button-1>", lambda e: show_connection_status())

# Alert icon and status (bottom-left) for grid issues
alert_frame = ttk.Frame(root)
alert_frame.grid(row=9, column=0, sticky='w', pady=10, padx=10)
alert_icon = ttk.Label(alert_frame, text="🏭", font=font_bold, cursor="hand2")
alert_icon.pack(side="left")
alert_status = ttk.Label(alert_frame, text="✔️", font=font_bold, cursor="hand2", width=2)
alert_status.pack(side="left")
alert_status.bind("<Button-1>", lambda e: show_grid_status())

# Configure grid to expand
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Start updating time and date
update_time()

# Start checking server connection, grid status, and bill updates
check_server_connection()
check_grid_status()
auto_update_bill()

# Run the application
root.mainloop()
