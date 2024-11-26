# MVC - View (using TKinter)
import sys
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.widgets import Meter
from random import choice
from datetime import datetime
from tkinter import messagebox
import logging

class UsageView:
  # Fonts
  font_reg = ("Verdana", 14, "normal")
  font_small = ("Verdana", 10, "normal")
  font_bold = ("Verdana", 16, "bold")
  font_heading = ("Verdana", 20, "bold")

  def __init__(self):
      self.target_usage = 0
      self.current_usage = 0
      self.launch_ui()
      
  # Set up logging configuration
  logging.basicConfig(filename="error_log.txt", level=logging.ERROR,
                      format="%(asctime)s - %(levelname)s - %(message)s")

  def launch_ui(self):
      # Create the main window with ttkbootstrap
      self.root = ttk.Window(themename="darkly")
      self.root.title("Smart Meter UI")
      self.root.geometry("900x600")
      self.root.minsize(900, 600)

      self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

      # Heading label
      lblHeading = ttk.Label(self.root, text="Smart Meter", font=UsageView.font_heading, anchor='center')
      lblHeading.grid(row=0, column=0, columnspan=3, pady=(10, 0))

      # Create and place the Meter (gauge) widget
      self.meter = Meter(
          self.root,
          metersize=180,
          amountused=self.current_usage,
          metertype='semi',
          subtext="Energy Usage",
          interactive=False,
          bootstyle="success",
          amounttotal=25
      )
      self.meter.grid(row=1, column=0, columnspan=3, pady=(10, 0))

      # Current budget and time display
      lblBudget = ttk.Label(self.root, text="Budget", font=UsageView.font_small)
      lblBudget.grid(row=5, column=0, columnspan=3)

      # Date label in the top-left
      self.lblDate = ttk.Label(self.root, text=datetime.now().strftime("%Y-%m-%d"), font=UsageView.font_bold)
      self.lblDate.grid(row=0, column=0, sticky='w', padx=10)

      # Time label in the top-right
      self.lblTime = ttk.Label(self.root, text=datetime.now().strftime("%H:%M"), font=UsageView.font_bold)
      self.lblTime.grid(row=0, column=2, sticky='e', padx=10)

      # Energy usage and bill labels
      lblUsage = ttk.Label(self.root, text="Energy Usage", font=UsageView.font_bold)
      lblUsage.grid(row=6, column=0)
      self.lblUsageVal = ttk.Label(self.root, text=f"{format(self.current_usage, '.1f')} kWh", font=UsageView.font_reg)
      self.lblUsageVal.grid(row=7, column=0)

      lblBill = ttk.Label(self.root, text="Bill", font=UsageView.font_bold)
      lblBill.grid(row=6, column=2)
      self.lblBillVal = ttk.Label(self.root, text=f"N/A", font=UsageView.font_reg)
      self.lblBillVal.grid(row=7, column=2)

      # Signal icon and status (bottom-right) for connection
      self.signal_frame = ttk.Frame(self.root)
      self.signal_frame.grid(row=9, column=2, sticky='e', pady=10, padx=10)
      self.signal_icon = ttk.Label(self.signal_frame, text="📶", font=UsageView.font_bold, cursor="hand2")
      self.signal_icon.pack(side="left")
      self.signal_status = ttk.Label(self.signal_frame, text="✔️", font=UsageView.font_bold, cursor="hand2", width=2)
      self.signal_status.pack(side="left")
      self.signal_status.bind("<Button-1>", lambda e: self.show_connection_status())

      # Alert icon and status (bottom-left) for grid issues
      self.alert_frame = ttk.Frame(self.root)
      self.alert_frame.grid(row=9, column=0, sticky='w', pady=10, padx=10)
      self.alert_icon = ttk.Label(self.alert_frame, text="🏭", font=UsageView.font_bold, cursor="hand2")
      self.alert_icon.pack(side="left")
      self.alert_status = ttk.Label(self.alert_frame, text="✔️", font=UsageView.font_bold, cursor="hand2", width=2)
      self.alert_status.pack(side="left")
      self.alert_status.bind("<Button-1>", lambda e: self.show_grid_status())

      # Separate error message labels for connection and grid issues
      self.lblConnectionError = ttk.Label(self.root, text="", font=UsageView.font_small, bootstyle="danger")
      self.lblConnectionError.grid(row=2, column=0, columnspan=3, pady=(5, 0))

      self.lblGridError = ttk.Label(self.root, text="", font=UsageView.font_small, bootstyle="danger")
      self.lblGridError.grid(row=3, column=0, columnspan=3, pady=(5, 0))

      # Configure grid to expand
      self.root.grid_columnconfigure(0, weight=1)
      self.root.grid_columnconfigure(1, weight=1)
      self.root.grid_columnconfigure(2, weight=1)

      # Start checking server connection, grid status, and bill updates
      self.update_time()
      return self.root, self.update_ui, self.update_server_connection


  # Function to smoothly update the gauge towards the target usage level
  def smooth_update(self):
      # Smoothly approach the target usage
      if self.current_usage < self.target_usage:
          self.current_usage += 3 if (self.target_usage - self.current_usage > 10) else 1 if (self.target_usage - self.current_usage > 1) else (self.target_usage - self.current_usage)  # Increment to increase
      elif self.current_usage > self.target_usage:
          self.current_usage -= 3 if (self.current_usage - self.target_usage > 10) else 1 if (self.current_usage - self.target_usage > 1) else (self.current_usage - self.target_usage)  # Decrement to decrease

      # Update the meter display and subtext
      self.meter.configure(amountused=format(self.current_usage, ".1f"), subtext="kWh")
      self.lblUsageVal.config(text=f"{format(self.current_usage, '.1f')} kWh")

      # Change color based on usage level
      if self.current_usage < 33:
          self.meter.configure(bootstyle="success")
      elif self.current_usage < 66:
          self.meter.configure(bootstyle="warning")
      else:
          self.meter.configure(bootstyle="danger")

      # Continue updating until reaching the target
      if self.current_usage != self.target_usage:
          self.root.after(25, self.smooth_update())  # Recursive call

  def update_ui(self, new_usage, new_bill):
      self.update_gauge(new_usage)
      self.update_bill(new_bill)

  # Function to set a new random target usage level
  def update_gauge(self, new_usage):
      self.target_usage = new_usage  # Set target
      self.smooth_update()  # Begin smooth transition

  def update_time(self):
      self.lblTime.config(text=datetime.now().strftime("%H:%M"))
      self.lblDate.config(text=datetime.now().strftime("%Y-%m-%d"))
      self.lblTime.after(5000, self.update_time)

  # Function to update the bill based on usage
  def update_bill(self, new_bill):
      self.lblBillVal.config(text=f"£{round(new_bill, 2)}")

  # Function to update connectivity status of server
  def update_server_connection(self, is_connected):
      if is_connected:
          self.connection_status = "strong"
          self.signal_status.config(text="✔️")
          self.lblConnectionError.config(text="")
      else:
          self.connection_status = "lost"
          self.signal_status.config(text="❌")
          self.lblConnectionError.config(text="Communication error with server", bootstyle="danger")
          logging.error("Communication error with server")  # Log error message

  # Function to update connectivity status of power grid
  def update_grid_connection(self, is_connected):
    if is_connected:
        self.grid_status = "no_issue"
        self.alert_status.config(text="✔️")
        self.lblGridError.config(text="")
    else:
        self.grid_status = "issue"
        self.alert_status.config(text="❌")
        self.lblGridError.config(text="Electricity grid issue detected", bootstyle="danger")
        logging.error("Electricity grid issue detected")  # Log grid issue

  # Function to show connection status on click
  def show_connection_status(self):
    status_message = "Connection strong" if self.connection_status == "strong" else "Connection lost"
    messagebox.showinfo("Connection Status", status_message)

  # Function to show grid status on click
  def show_grid_status(self):
      grid_message = "Electricity grid is stable" if self.grid_status == "no_issue" else "Electricity grid issue detected"
      messagebox.showinfo("Grid Status", grid_message)

  def on_closing(self):
      print("Shutdown")
      sys.exit() # closes index.py as well

  def run(self):
      self.root.mainloop()
