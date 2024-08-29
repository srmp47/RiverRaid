import tkinter as tk
from tkinter import messagebox
def submit_username():
    username = entry_username.get()  # Get the username from the entry widget
    if username:
        messagebox.showinfo("Username Submitted", f"Your username is: {username}")
    else:
        messagebox.showwarning("Input Error", "Please enter a username.")
root = tk.Tk()
root.title("Login menu")
root.resizable(width=False, height=False)
root.geometry("1400x800")

label = tk.Label(root, text="Enter your username:")
label.pack(pady=10)  # Add some vertical padding
label = tk.Label(root, text="Enter your password")
# Create an entry widget for user input
entry_username = tk.Entry(root)
entry_username.pack(pady=5)  # Add some vertical padding

label = tk.Label(root, text="Enter your password:")
label.pack(pady=10)
entry_password = tk.Entry(root)
entry_password.pack(pady=5)
submit_button = tk.Button(root, text="Submit", command=submit_username)
submit_button.pack(pady=20)

root.mainloop()