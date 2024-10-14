import tkinter as tk
from tkinter import messagebox

# Define the correct username and password
user2mdp = dict(zip(["fbb", "zcl", "lydz", "zts", "hzj", "wbb"], range(6)))
print(user2mdp)

# Function to validate login
def validate_login():
    username = entry_username.get()
    password = entry_password.get()

    if username not in user2mdp:
        messagebox.showerror("Login Status", "Invalid username")
        return
    if password == str(user2mdp[username]):
        messagebox.showinfo("Login Status", "Login successful!")
    else:
        messagebox.showerror("Login Status", "Invalid password.")


# Create the main window
root = tk.Tk()
root.title("Login")

# Create and place the username label and entry
label_username = tk.Label(root, text="Username:")
label_username.pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=10)

# Create and place the password label and entry
label_password = tk.Label(root, text="Password:")
label_password.pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=10)

# Create and place the login button
button_login = tk.Button(root, text="Login", command=validate_login)
button_login.pack(pady=20)

# Start the GUI event loop
root.mainloop()