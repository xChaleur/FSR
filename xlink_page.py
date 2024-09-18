import tkinter as tk

# Function to return to the main window (for now just quits the xLink page)
def quit_xlink():
    root.destroy()

# Create the xLink page window
root = tk.Tk()
root.title("xLink")
root.geometry("600x600")

# Add content to the xLink window
label = tk.Label(root, text="Welcome to the xLink page", font=("Arial", 16))
label.pack(pady=20)

# Add more content specific to xLink here (buttons, labels, etc.)
description_label = tk.Label(root, text="This is where you can add xLink specific settings or actions.")
description_label.pack(pady=10)

# Quit button to close xLink page
quit_button = tk.Button(root, text="Quit xLink", command=quit_xlink)
quit_button.pack(pady=20)

# Start the xLink window loop
root.mainloop()
