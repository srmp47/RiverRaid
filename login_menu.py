import tkinter as tk
from tkinter import messagebox
import login_menu_controller

def login_user():
    username = entry_username.get()  # Get the username from the entry widget
    password = str(entry_password.get())  # Get the password from the entry widget
    if login_menu_controller.username_exists(username) and  not login_menu_controller.is_password_correct(username, password):
        messagebox.showwarning("Wrong Password", "Your password is wrong!")
    elif not login_menu_controller.username_exists(username):
        messagebox.showwarning("Username not exists", "Please enter a  correct username.")
    else:
        messagebox.showinfo("Logged in successfully", "You logged In.\nPlease Wait ...")
def register_user():
    username = entry_username.get()
    password = entry_password.get()
    if username == "":
        messagebox.showwarning("Empty Username", "Please enter a username")
    elif password == "":
        messagebox.showwarning("Empty Password", "Please enter a password")
    elif login_menu_controller.username_exists(username):
        messagebox.showwarning("Username Exists", "This username exists.\nPlease enter a new username")
    else:
        messagebox.showinfo("Registered successfully", "You registered.\nPlease Wait ...")
        login_menu_controller.add_user(username, password, 0)



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
submit_button = tk.Button(root, text="Login", command=login_user)
submit_button.pack(pady=20)
submit_button = tk.Button(root, text="Register", command=register_user)
submit_button.pack(pady=10)

root.mainloop()
