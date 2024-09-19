import os
import sys
import shutil
import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, Checkbutton, IntVar

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_default_locations():
    global default_folder_1, default_folder_2, default_folder_3
    if DEFAULT_LOCATIONS_FILE.exists():
        with open(DEFAULT_LOCATIONS_FILE, 'r') as file:
            data = json.load(file)
            # Load the data as before
    else:
        # Initialize default folders to None or default values
        default_folder_1 = None
        default_folder_2 = None
        default_folder_3 = None

def save_default_locations():
    global default_folder_1, default_folder_2, default_folder_3
    data = {
        "default_folder_1": str(default_folder_1) if default_folder_1 else None,
        "default_folder_2": str(default_folder_2) if default_folder_2 else None,
        "default_folder_3": str(default_folder_3) if default_folder_3 else None
    }
    with open(DEFAULT_LOCATIONS_FILE, 'w') as file:
        json.dump(data, file)
    messagebox.showinfo("Saved", "Default folder locations have been saved.")


# Path to save the default folder locations
DEFAULT_LOCATIONS_FILE = Path(resource_path("default_locations.json"))

# Global variables for RADA Tools
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

# Function to save default folder locations to a file
def save_default_locations():
    global default_folder_1, default_folder_2, default_folder_3
    data = {
        "default_folder_1": str(default_folder_1) if default_folder_1 else None,
        "default_folder_2": str(default_folder_2) if default_folder_2 else None,
        "default_folder_3": str(default_folder_3) if default_folder_3 else None
    }
    with open(DEFAULT_LOCATIONS_FILE, 'w') as file:
        json.dump(data, file)
    messagebox.showinfo("Saved", "Default folder locations have been saved.")

# Function to move files with the selected extensions
def move_files_with_extensions(source_folder, extensions):
    try:
        if not source_folder or not source_folder.exists():
            messagebox.showerror("Folder Error", "The selected folder no longer exists.")
            return

        downloads_folder = Path.home() / "Downloads"
        files_moved_total = 0

        for ext in extensions:
            new_folder = downloads_folder / f"moved_files_{ext.strip('.')}"
            new_folder.mkdir(exist_ok=True)

            files_moved = 0
            for file in source_folder.glob(f"*.{ext.strip('.')}"):
                shutil.move(str(file), new_folder)
                files_moved += 1
                files_moved_total += 1

        if files_moved_total > 0:
            messagebox.showinfo("Success", f"Moved {files_moved_total} files with selected extensions to {downloads_folder}")
        else:
            messagebox.showinfo("No Files Found", "No files with the selected extensions were found in the selected folder.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to select a folder
def select_folder():
    global selected_folder
    selected_folder_path = filedialog.askdirectory(title="Select Folder")

    if selected_folder_path:
        selected_folder = Path(selected_folder_path)
        folder_label.config(text=f"Current Folder: {selected_folder}")
    else:
        messagebox.showwarning("Folder Error", "No folder selected!")

# Function to select Default Folder 1 manually
def select_default_folder_1():
    global default_folder_1
    selected_default_folder_path = filedialog.askdirectory(title="Select Default Folder 1")
    if selected_default_folder_path:
        default_folder_1 = Path(selected_default_folder_path)
        default_folder_1_label.config(text=f"Default Folder 1: {default_folder_1}")
        default_folder_1_label.pack(side=tk.LEFT)

# Function to select Default Folder 2 manually
def select_default_folder_2():
    global default_folder_2
    selected_default_folder_2_path = filedialog.askdirectory(title="Select Default Folder 2")
    if selected_default_folder_2_path:
        default_folder_2 = Path(selected_default_folder_2_path)
        default_folder_2_label.config(text=f"Default Folder 2: {default_folder_2}")
        default_folder_2_label.pack(side=tk.LEFT)

# Function to select Default Folder 3 manually
def select_default_folder_3():
    global default_folder_3
    selected_default_folder_3_path = filedialog.askdirectory(title="Select Default Folder 3")
    if selected_default_folder_3_path:
        default_folder_3 = Path(selected_default_folder_3_path)
        default_folder_3_label.config(text=f"Default Folder 3: {default_folder_3}")
        default_folder_3_label.pack(side=tk.LEFT)

# Function to display a prompt and allow selection of multiple extensions
def select_multiple_extensions(extensions):
    def on_confirm():
        global selected_extensions
        selected_extensions = [ext for ext, var in checkboxes.items() if var.get() == 1]
        if selected_extensions:
            folder_to_use = default_folder_1 if default_folder_1 else selected_folder
            move_files_with_extensions(folder_to_use, selected_extensions)
        else:
            messagebox.showwarning("No Selection", "No extensions selected.")
        extension_window.destroy()

    extension_window = tk.Toplevel(root)
    extension_window.title("Select Extensions")
    extension_window.geometry("300x400")

    checkboxes = {}
    for ext in extensions:
        var = IntVar()
        check = tk.Checkbutton(extension_window, text=ext, variable=var)
        check.pack(anchor=tk.W)
        checkboxes[ext] = var

    confirm_button = tk.Button(extension_window, text="Confirm", command=on_confirm)
    confirm_button.pack(pady=10)

# Function to list all unique file extensions in the selected folder and open the selection window
def list_extensions():
    global selected_folder
    if selected_folder is None:
        messagebox.showwarning("Folder Error", "No folder selected!")
        return

    extensions = set()
    for file in selected_folder.iterdir():
        if file.is_file():
            extensions.add(file.suffix)

    if extensions:
        select_multiple_extensions(extensions)
    else:
        messagebox.showinfo("No Files Found", "No files found in the selected folder.")

# Function to clear the selected folder and extensions
def clear_selections():
    global selected_folder, default_folder_1, default_folder_2, default_folder_3, selected_extensions
    selected_folder = None
    default_folder_1 = None
    default_folder_2 = None
    default_folder_3 = None
    selected_extensions = []
    folder_label.config(text="Current Folder: None")
    default_folder_1_label.pack_forget()
    default_folder_2_label.pack_forget()
    default_folder_3_label.pack_forget()

# Function to show the main page of RADA Tools
def show_main_page():
    for widget in main_frame.winfo_children():
        widget.destroy()
    main_page_content()

# Function to build the main page content of RADA Tools
def main_page_content():
    # Button to select a folder
    select_folder_button = tk.Button(main_frame, text="Select Folder", command=select_folder)
    select_folder_button.pack(padx=10, pady=10)

    # Button to move files
    move_files_button = tk.Button(main_frame, text="Move Files", command=lambda: move_files_with_extensions(default_folder_1 if default_folder_1 else selected_folder, selected_extensions))
    move_files_button.pack(padx=10, pady=10)

    # Frame for Folder display
    folder_frame = tk.Frame(main_frame)
    folder_frame.pack(padx=10, pady=5)

    # Label to display the current selected folder (initially cleared)
    global folder_label
    folder_label = tk.Label(folder_frame, text="Current Folder: None")
    folder_label.pack(side=tk.LEFT)

    # Labels for Default Folders (initially hidden)
    global default_folder_1_label, default_folder_2_label, default_folder_3_label
    default_folder_1_label = tk.Label(folder_frame, text="")
    default_folder_2_label = tk.Label(folder_frame, text="")
    default_folder_3_label = tk.Label(folder_frame, text="")

    # Button to clear the selected folder, default folders, and extensions
    clear_button = tk.Button(main_frame, text="Clear Selections", command=clear_selections, fg="red", padx=5)
    clear_button.pack(padx=10, pady=10)

# Function to switch to the FSR page within the same window
def open_fsr_page():
    # Clear the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()
    # Build the FSR interface
    open_fsr()

# FSR Global variables
fsr_destination_a = None
fsr_destination_b = None
fsr_source = None

# Function to select Destination A
def select_fsr_destination_a():
    global fsr_destination_a
    folder = filedialog.askdirectory(title="Select Destination A Folder")
    if folder:
        fsr_destination_a = folder
        fsr_destination_a_label.config(text=f"Destination A: {fsr_destination_a}")
    else:
        messagebox.showwarning("Folder Error", "No folder selected for Destination A!")

# Function to select Destination B
def select_fsr_destination_b():
    global fsr_destination_b
    folder = filedialog.askdirectory(title="Select Destination B Folder")
    if folder:
        fsr_destination_b = folder
        fsr_destination_b_label.config(text=f"Destination B: {fsr_destination_b}")
    else:
        messagebox.showwarning("Folder Error", "No folder selected for Destination B!")

# Function to select Source
def select_fsr_source():
    global fsr_source
    folder = filedialog.askdirectory(title="Select Source Folder")
    if folder:
        fsr_source = folder
        fsr_source_label.config(text=f"Source: {fsr_source}")
    else:
        messagebox.showwarning("Folder Error", "No folder selected for Source!")

# Function to scan files for the radar update
def scan_fsr_files():
    if not fsr_destination_a or not fsr_destination_b:
        messagebox.showwarning("Folder Error", "Please select Destination A and Destination B!")
    else:
        messagebox.showinfo("Scan Files", "Scanning files for update...")

# Function to update radar files
def update_radar():
    if not fsr_source:
        messagebox.showwarning("Folder Error", "Please select Source!")
    else:
        messagebox.showinfo("Update Radar", "Radar files have been updated successfully!")

# Function to open the FSR interface
def open_fsr():
    # Clear the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Destination A Selection
    global fsr_destination_a_label
    fsr_destination_a_label = tk.Label(main_frame, text="Destination A: None")
    fsr_destination_a_label.pack(padx=10, pady=5)
    select_fsr_destination_a_button = tk.Button(main_frame, text="Select Destination A", command=select_fsr_destination_a)
    select_fsr_destination_a_button.pack(padx=10, pady=5)

    # Destination B Selection
    global fsr_destination_b_label
    fsr_destination_b_label = tk.Label(main_frame, text="Destination B: None")
    fsr_destination_b_label.pack(padx=10, pady=5)
    select_fsr_destination_b_button = tk.Button(main_frame, text="Select Destination B", command=select_fsr_destination_b)
    select_fsr_destination_b_button.pack(padx=10, pady=5)

    # Source Selection
    global fsr_source_label
    fsr_source_label = tk.Label(main_frame, text="Source: None")
    fsr_source_label.pack(padx=10, pady=5)
    select_fsr_source_button = tk.Button(main_frame, text="Select Source", command=select_fsr_source)
    select_fsr_source_button.pack(padx=10, pady=5)

    # Scan Files Button
    scan_files_button = tk.Button(main_frame, text="Scan Files", command=scan_fsr_files)
    scan_files_button.pack(padx=10, pady=10)

    # Update Radar Button
    update_radar_button = tk.Button(main_frame, text="Update Radar", command=update_radar)
    update_radar_button.pack(padx=10, pady=10)

    # Back Button to return to RADA Tools main page
    back_button = tk.Button(main_frame, text="Back to RADA Tools", command=show_main_page)
    back_button.pack(padx=10, pady=10)

# Menu action for quitting the app
def quit_app():
    root.quit()

# Menu action for opening an "About" dialog
def show_about():
    messagebox.showinfo("About", "RADA Tools Application\nVersion 1.0\nCreated by John Alingwa")

# Create the GUI application
root = tk.Tk()
root.title("RADA Tools")
root.geometry("600x600")
root.resizable(False, False)

# Create a frame to hold all content
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Load default locations if they exist
load_default_locations()

# Create a menu bar
menu_bar = tk.Menu(root)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Save Default Locations", command=save_default_locations)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=quit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

# Options menu
options_menu = tk.Menu(menu_bar, tearoff=0)
options_menu.add_command(label="FSR", command=open_fsr_page)  # Link FSR to the menu option
options_menu.add_command(label="List Extensions in Folder", command=list_extensions)

# Submenu for default folders
default_folders_menu = tk.Menu(options_menu, tearoff=0)
default_folders_menu.add_command(label="Select Default Folder 1", command=select_default_folder_1)
default_folders_menu.add_command(label="Select Default Folder 2", command=select_default_folder_2)
default_folders_menu.add_command(label="Select Default Folder 3", command=select_default_folder_3)
options_menu.add_cascade(label="Default Folders", menu=default_folders_menu)

menu_bar.add_cascade(label="Options", menu=options_menu)

# Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Add the menu bar to the root window
root.config(menu=menu_bar)

# Build the main page content
main_page_content()

# Start the application loop
root.mainloop()
