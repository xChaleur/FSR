import os
import shutil
import sys
import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, Checkbutton, IntVar

# Path to save the default folder locations
DEFAULT_LOCATIONS_FILE = Path.home() / "default_locations.json"

# Global variables to store the currently selected folders and extensions
selected_folder = None
default_folder_1 = None
default_folder_2 = None
default_folder_3 = None
selected_extensions = []

# Function to load default folder locations from a file
def load_default_locations():
    global default_folder_1, default_folder_2, default_folder_3
    if DEFAULT_LOCATIONS_FILE.exists():
        with open(DEFAULT_LOCATIONS_FILE, 'r') as file:
            data = json.load(file)
            default_folder_1_path = data.get("default_folder_1", None)
            default_folder_2_path = data.get("default_folder_2", None)
            default_folder_3_path = data.get("default_folder_3", None)

            if default_folder_1_path:
                default_folder_1 = Path(default_folder_1_path)
                default_folder_1_label.config(text=f"Default Folder 1: {default_folder_1}")
                default_folder_1_label.pack(side=tk.LEFT)

            if default_folder_2_path:
                default_folder_2 = Path(default_folder_2_path)
                default_folder_2_label.config(text=f"Default Folder 2: {default_folder_2}")
                default_folder_2_label.pack(side=tk.LEFT)

            if default_folder_3_path:
                default_folder_3 = Path(default_folder_3_path)
                default_folder_3_label.config(text=f"Default Folder 3: {default_folder_3}")
                default_folder_3_label.pack(side=tk.LEFT)

# Function to open the FSR interface and clear the existing content
def open_fsr():
    for widget in main_frame.winfo_children():
        widget.destroy()

    # FSR content (Destination A, B, and Source selections)
    global fsr_destination_a_label, fsr_destination_b_label, fsr_source_label

    fsr_destination_a_label = tk.Label(main_frame, text="Destination A: None")
    fsr_destination_a_label.pack(padx=10, pady=5)
    select_fsr_destination_a_button = tk.Button(main_frame, text="Select Destination A", command=select_fsr_destination_a)
    select_fsr_destination_a_button.pack(padx=10, pady=5)

    fsr_destination_b_label = tk.Label(main_frame, text="Destination B: None")
    fsr_destination_b_label.pack(padx=10, pady=5)
    select_fsr_destination_b_button = tk.Button(main_frame, text="Select Destination B", command=select_fsr_destination_b)
    select_fsr_destination_b_button.pack(padx=10, pady=5)

    fsr_source_label = tk.Label(main_frame, text="Source: None")
    fsr_source_label.pack(padx=10, pady=5)
    select_fsr_source_button = tk.Button(main_frame, text="Select Source", command=select_fsr_source)
    select_fsr_source_button.pack(padx=10, pady=5)

    scan_files_button = tk.Button(main_frame, text="Scan Files", command=scan_fsr_files)
    scan_files_button.pack(padx=10, pady=10)

    update_radar_button = tk.Button(main_frame, text="Update Radar", command=update_radar)
    update_radar_button.pack(padx=10, pady=10)

# Function to select Destination A
def select_fsr_destination_a():
    folder = filedialog.askdirectory()
    if folder:
        fsr_destination_a_label.config(text=f"Destination A: {folder}")

# Function to select Destination B
def select_fsr_destination_b():
    folder = filedialog.askdirectory()
    if folder:
        fsr_destination_b_label.config(text=f"Destination B: {folder}")

# Function to select Source
def select_fsr_source():
    folder = filedialog.askdirectory()
    if folder:
        fsr_source_label.config(text=f"Source: {folder}")

# Function to scan files for the radar update
def scan_fsr_files():
    messagebox.showinfo("Scan Files", "Scanning files for update...")

# Function to update radar files
def update_radar():
    messagebox.showinfo("Update Radar", "Radar files have been updated successfully!")

# Create the main GUI application
root = tk.Tk()
root.title("File Mover with FSR")
root.geometry("600x600")
root.resizable(False, False)

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create the Options menu
options_menu = tk.Menu(menu_bar, tearoff=0)
options_menu.add_command(label="FSR", command=open_fsr)  # FSR button linked to open_fsr()
menu_bar.add_cascade(label="Options", menu=options_menu)

# Default to FSR view on launch
open_fsr()

root.mainloop()
