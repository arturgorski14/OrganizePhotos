import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Top and Bottom Frame Example")
root.geometry("400x300")  # Set a fixed size for the window

# Create the top frame
top_frame = tk.Frame(root, bg="lightgray", height=100)
top_frame.pack(side="top", fill="x")  # Pack at the top and fill the width

# Create two buttons inside the top frame
button1 = tk.Button(top_frame, text="Button 1")
button1.pack(
    side="left", expand=True, fill="both"
)  # Fill horizontally and expand to take up space

button2 = tk.Button(top_frame, text="Button 2")
button2.pack(
    side="left", expand=True, fill="both"
)  # Fill horizontally and expand to take up space

# Create the bottom frame
bottom_frame = tk.Frame(root, bg="lightblue", height=200)
bottom_frame.pack(
    side="bottom", fill="both", expand=True
)  # Pack at the bottom and fill the remaining space

# Add any widget you want to the bottom frame (as an example, a label)
label = tk.Label(bottom_frame, text="Bottom Frame Content", bg="lightblue")
label.pack(pady=20)

# Run the main event loop
root.mainloop()
