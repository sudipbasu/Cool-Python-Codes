import tkinter as tk
from tkinter import messagebox
import socket

# Function to fetch IP Address
def get_ip():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return

    try:
        ip_address = socket.gethostbyname(url)
        result_label.config(text=f"IP Address: {ip_address}", fg="green")
    except socket.gaierror:
        result_label.config(text="Invalid URL or network error.", fg="red")

# Main Window
root = tk.Tk()
root.title("IP Finder")
root.geometry("500x300")
root.resizable(False, False)
root.configure(bg="#e8f0f2")

# Header Frame
header_frame = tk.Frame(root, bg="#007BFF")
header_frame.pack(fill="x")
header_label = tk.Label(header_frame, text="IP Address Finder", font=("Arial", 20, "bold"), bg="#007BFF", fg="white")
header_label.pack(pady=10)

# Content Frame
content_frame = tk.Frame(root, bg="#e8f0f2")
content_frame.pack(pady=20)

# URL Entry Label
url_label = tk.Label(content_frame, text="Enter URL:", font=("Arial", 14), bg="#e8f0f2", fg="#333")
url_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

# URL Entry Field
url_entry = tk.Entry(content_frame, font=("Arial", 14), width=30, bd=2, relief="solid")
url_entry.grid(row=0, column=1, pady=10, padx=10)

# Find Button
find_button = tk.Button(content_frame, text="Find IP", font=("Arial", 14, "bold"), bg="#28a745", fg="white", bd=0, padx=15, pady=5, relief="flat", command=get_ip)
find_button.grid(row=1, columnspan=2, pady=20)

# Result Label
result_label = tk.Label(content_frame, text="", font=("Arial", 14), bg="#e8f0f2")
result_label.grid(row=2, columnspan=2, pady=10)

# Footer Frame
footer_frame = tk.Frame(root, bg="#007BFF")
footer_frame.pack(fill="x", side="bottom")
footer_label = tk.Label(footer_frame, text="Powered by Tkinter", font=("Arial", 10, "italic"), bg="#007BFF", fg="white")
footer_label.pack(pady=5)

root.mainloop()
