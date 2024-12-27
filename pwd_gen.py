import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

# Function to generate a random password
def generate_password():
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError("Length must be a positive integer.")

        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        
        password_entry.config(state="normal")  # Enable editing
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)
        password_entry.config(state="readonly")  # Make it readonly again
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Function to copy the password to the clipboard
def copy_to_clipboard():
    password = password_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        root.update()  # Keep clipboard data even after program closes
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "No password to copy!")

# Initialize the tkinter window
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("400x250")
root.resizable(False, False)

# Styling using ttk
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))
style.configure("TEntry", font=("Arial", 12))

# UI Elements with better layout
frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

length_label = ttk.Label(frame, text="Password Length:")
length_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

length_entry = ttk.Entry(frame, width=10)
length_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

generate_button = ttk.Button(frame, text="Generate Password", command=generate_password)
generate_button.grid(row=1, column=0, columnspan=2, pady=10, sticky=tk.EW)

password_label = ttk.Label(frame, text="Generated Password:")
password_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

password_entry = ttk.Entry(frame, width=30, state="readonly")
password_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

copy_button = ttk.Button(frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=3, column=0, columnspan=2, pady=10, sticky=tk.EW)

# Run the application
root.mainloop()
