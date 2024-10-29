import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

arc_length = 0.8 * np.pi
arc_angle = np.pi / -1.1

def draw_gauge(ax, value, max_value):
    ax.clear()
    ax.set_theta_offset(arc_angle) # start angle
    ax.set_theta_direction(-1) # clockwise
    ax.set_ylim(0, 1)
    ax.set_xlim(0, arc_length) # arc
    ax.axis('off')

    # Draw the gauge background
    ax.barh(1, arc_length, height=0.3, color='lightgrey', edgecolor='white')
    # Draw the gauge value
    ax.barh(1, (value / max_value) * arc_length, height=0.3, color='green', edgecolor='white')
    # Add text
    ax.text(0, 0, f'{value}%', ha='center', va='center', fontsize=20, color='white')

class GaugeFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Create a Matplotlib figure
        self.fig = Figure(figsize=(1.5, 1.5), dpi=100, facecolor='black')
        self.ax = self.fig.add_subplot(111, polar=True)

        # Draw initial gauge
        draw_gauge(self.ax, 30, 100)

        # Embed the Matplotlib figure in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add a button to update the gauge
        self.update_button = tk.Button(self, text="Update Gauge", command=self.update_gauge)
        self.update_button.pack(side=tk.BOTTOM)

    def update_gauge(self):
        # Update the gauge with a new value
        new_value = np.random.randint(0, 101)
        draw_gauge(self.ax, new_value, 100)
        self.canvas.draw()
