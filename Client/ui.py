import tkinter as tk

from gauge import GaugeFrame

font_reg = ("Verdana", 14, "normal")
font_small = ("Verdana", 10, "normal")
font_bold = ("Verdana", 16, "bold")
font_heading = ("Verdana", 20, "bold")

# Create the main window
root = tk.Tk()
root.title("Basic Tkinter App")
root.geometry("400x300")
root.minsize(400, 300)
root.configure(bg='black')

# label widget
lblHeading = tk.Label(root, text="Smart Meter", bg='black', fg='white', font=font_heading, anchor='center')
lblHeading.grid(row=0, columnspan=2)

lblUsage = tk.Label(root, text="Energy Usage", bg='black', fg='white', font=font_bold)
lblUsage.grid(row=1, column=0, pady=20)
lblUsageVal = tk.Label(root, text="Energy Usage", bg='black', fg='white', font=font_reg)
lblUsageVal.grid(row=2, column=0)

lblBill = tk.Label(root, text="Bill", bg='black', fg='white', font=font_bold)
lblBill.grid(row=1, column=1)
lblBill = tk.Label(root, text="£10.11", bg='black', fg='white', font=font_reg)
lblBill.grid(row=2, column=1)

# Create and place the GaugeFrame
gauge_frame = GaugeFrame(root)
gauge_frame.grid(row=3, column=0)

# Configure grid to expand
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Run the application
root.mainloop()
