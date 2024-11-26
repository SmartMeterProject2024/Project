import sys
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.widgets import Meter
from random import choice
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

# Variables to store usage, target usage
target_usage = 0
current_usage = 0

def launch_ui():
    global root, meter, current_usage, target_usage, lblUsageVal, lblTime, lblDate, lblBillVal, signal_status, alert_status, lblGridError, lblConnectionError, signal_icon, alert_icon, style
    # Create the main window with ttkbootstrap
    root = ttk.Window(themename="darkly")
    
    style = ttk.Style()
    style.configure("success.TLabel", foreground="green", font=font_bold)
    style.configure("danger.TLabel", foreground="red", font=font_bold)

    root.title("Smart Meter UI")
    root.geometry("900x600")
    root.minsize(900, 600)

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
        bootstyle="success",
        amounttotal=25
    )
    meter.grid(row=1, column=0, columnspan=3, pady=(10, 0))

    # Current budget and time display
    lblBudget = ttk.Label(root, text="Budget", font=font_small)
    lblBudget.grid(row=5, column=0, columnspan=3)

    # Date label in the top-left
    lblDate = ttk.Label(root, text=datetime.now().strftime("%Y-%m-%d"), font=font_bold)
    lblDate.grid(row=0, column=0, sticky='w', padx=10)

    # Time label in the top-right
    lblTime = ttk.Label(root, text=datetime.now().strftime("%H:%M"), font=font_bold)
    lblTime.grid(row=0, column=2, sticky='e', padx=10)

    # Energy usage and bill labels
    lblUsage = ttk.Label(root, text="Energy Usage", font=font_bold)
    lblUsage.grid(row=6, column=0)
    lblUsageVal = ttk.Label(root, text=f"{format(current_usage, '.1f')} kWh", font=font_reg)
    lblUsageVal.grid(row=7, column=0)

    lblBill = ttk.Label(root, text="Bill", font=font_bold)
    lblBill.grid(row=6, column=2)
    lblBillVal = ttk.Label(root, text=f"N/A", font=font_reg)
    lblBillVal.grid(row=7, column=2)

    # Button to update gauge randomly
    #btnRandomUsage = ttk.Button(root, text="Randomise Usage", bootstyle="outline-light", command=update_gauge)
    #btnRandomUsage.grid(row=8, column=0, columnspan=3, pady=20)

    # Signal icon and status (bottom-right) for connection
    signal_frame = ttk.Frame(root)
    signal_frame.grid(row=9, column=2, sticky='e', pady=10, padx=10)
    signal_icon = ttk.Label(signal_frame, text="📶", font=font_bold, cursor="hand2")
    signal_icon.pack(side="left")
    signal_icon.bind("<Button-1>", lambda e: show_connection_status())

    # Alert icon and status (bottom-left) for grid issues
    alert_frame = ttk.Frame(root)
    alert_frame.grid(row=9, column=0, sticky='w', pady=10, padx=10)
    alert_icon = ttk.Label(alert_frame, text="🏭", font=font_bold, cursor="hand2")
    alert_icon.pack(side="left")
    alert_icon.bind("<Button-1>", lambda e: show_grid_status())

    # Separate error message labels for connection and grid issues
    lblConnectionError = ttk.Label(root, text="", font=font_small, bootstyle="danger")
    lblConnectionError.grid(row=2, column=0, columnspan=3, pady=(5, 0))

    lblGridError = ttk.Label(root, text="", font=font_small, bootstyle="danger")
    lblGridError.grid(row=3, column=0, columnspan=3, pady=(5, 0))

    # Configure grid to expand
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

    # Start checking server connection, grid status, and bill updates
    update_time()
    check_grid_status()
    return root, update_ui, update_server_connection


# Function to smoothly update the gauge towards the target usage level
def smooth_update():
    global current_usage
    # Smoothly approach the target usage
    if current_usage < target_usage:
        current_usage += 3 if (target_usage - current_usage > 10) else 1 if (target_usage - current_usage > 1) else (target_usage - current_usage)  # Increment to increase
    elif current_usage > target_usage:
        current_usage -= 3 if (current_usage - target_usage > 10) else 1 if (current_usage - target_usage > 1) else (current_usage - target_usage)  # Decrement to decrease

    # Update the meter display and subtext
    meter.configure(amountused=format(current_usage, ".2f"), subtext="kWh")
    lblUsageVal.config(text=f"{format(current_usage, '.2f')} kWh")

    # Change color based on usage level
    if current_usage < 33:
        meter.configure(bootstyle="success")
    elif current_usage < 66:
        meter.configure(bootstyle="warning")
    else:
        meter.configure(bootstyle="danger")

    # Continue updating until reaching the target
    if current_usage != target_usage:
        root.after(25, smooth_update)  # Recursive call

def update_ui(new_usage, new_bill):
    update_gauge(new_usage)
    update_bill(new_bill)

# Function to set a new random target usage level
def update_gauge(new_usage):
    global target_usage
    target_usage = new_usage  # Set target
    smooth_update()  # Begin smooth transition

def update_time():
    lblTime.config(text=datetime.now().strftime("%H:%M"))
    lblDate.config(text=datetime.now().strftime("%Y-%m-%d"))
    lblTime.after(5000, update_time)

# Function to update the bill based on usage
def update_bill(new_bill):
    lblBillVal.config(text=f"£{format(new_bill, '.2f')}")

def update_server_connection(is_connected):
    global connection_status, signal_icon
    if is_connected:
        connection_status = "strong"
        lblConnectionError.config(text="")
        signal_icon.config(style="success.TLabel")
    else:
        connection_status = "lost"
        lblConnectionError.config(text="Communication error with server", bootstyle="danger")
        signal_icon.config(style="danger.TLabel")
        logging.error("Communication error with server")  # Log error message

# Function to simulate grid status check
def check_grid_status():
    global grid_status
    grid_issue = choice([True, False])  # Simulate grid status
    if grid_issue:
        grid_status = "issue"
        lblGridError.config(text="Electricity grid issue detected", bootstyle="danger")
        alert_icon.config(style="danger.TLabel")
        logging.error("Electricity grid issue detected")  # Log grid issue
    else:
        grid_status = "no_issue"
        lblGridError.config(text="")
        alert_icon.config(style="success.TLabel")
    
    root.after(15000, check_grid_status)

# Function to show connection status on click
def show_connection_status():
    status_message = "Connection strong" if connection_status == "strong" else "Connection lost"
    messagebox.showinfo("Connection Status", status_message)

# Function to show grid status on click
def show_grid_status():
    grid_message = "Electricity grid is stable" if grid_status == "no_issue" else "Electricity grid issue detected"
    messagebox.showinfo("Grid Status", grid_message)

def on_closing():
    print("Shutdown")
    sys.exit() # closes index.py as well
