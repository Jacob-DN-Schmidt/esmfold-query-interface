import threading
import queue
import tkinter as tk
import os
import re
import sys
import time
from time import sleep as wait
from tkinter import ttk
from tkinter import font
from tkinter import scrolledtext as st
from ESMFold_Xmer_Query_Interface import *


window = tk.Tk()
window.title("ESMFold Query Interface")
window.state("zoomed")

window.resizable(True, True)
window.option_add("*Font", "Calibri 12")
window.option_add("*Label.justify", "left")


default_font = font.Font(family="Calibri", size=12)
default_style = ttk.Style()
default_style.configure("Treeview.Heading", font="Calibri 12")


f_debug_section = ttk.Frame(master=window)
st_debug = st.ScrolledText(master=f_debug_section, font=("Calibri", 12), state="disabled")
st_debug.pack(fill="both", expand=True)

f_debug_section.pack(fill="both", expand=True)

def debug_print(msg: str):
    st_debug.config(state="normal")
    st_debug.insert(tk.END, msg + "\n")
    st_debug.see(tk.END)
    st_debug.config(state="disabled")
    st_debug.update()

def do_something(data: int, result_queue: queue.Queue) -> None:
    """Simulate a task that processes data and puts the result in a queue."""
    result = data * 2  # Example processing
    wait(10)  # Simulate a delay
    result_queue.put(result)

window.bind("<space>", lambda event: on_space_press()) 

def on_space_press():
    result_queue = queue.Queue()
    debug_print("Starting tasks...")

    for i in range(5):
        debug_print(f"Starting task {i}")
        thread = threading.Thread(target=do_something, args=(i, result_queue))
        thread.start()
        while thread.is_alive():
            debug_print(f"  Task {i} is still running...")
            wait(1)
        thread.join()  # Wait for the thread to finish
        debug_print(f"  Result: {result_queue.get()}")

    debug_print("All tasks completed.")

window.mainloop()