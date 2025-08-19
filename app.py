import tkinter as tk
from tkinter import font

root = tk.Tk()
root.geometry("1200x850")
root.title("Offline Password Manager")

# Configure grid layout
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=1)

# Column configuration
for col in range(5):
    # 5 columns: website, username, password, copy, reveal
    root.grid_columnconfigure(col, weight=1)

# Fonts
header_font = ("Helvetica", 28, "bold")
entry_font = ("Arial", 14)
button_font = ("Calibri", 16)
stored_header_font = ("Helvetica", 18, "bold")
header_font = ("Arial", 14, "bold")
cell_font = ("Arial", 12)

# Sample data
data = [
    {"website": "example.com", "username": "john_doe", "password": "MySecurePass123"},
    {"website": "gmail.com", "username": "jane123", "password": "Another$ecret"},
    {"website": "github.com", "username": "coder007", "password": "Code@2023"},
]

# Header Label (centered)
header = tk.Label(root, text="Offline Password Manager", font=header_font)
header.grid(row=0, column=0, columnspan=3, pady=40, sticky="n")

# Label: placeholder label (inside Entry workaround)
placeholder = tk.Label(root, text="Enter Master Password", font=("Arial", 12))
placeholder.grid(row=1, column=0, padx=(40, 10), sticky="e")

# Master password entry
password_entry = tk.Entry(root, font=entry_font, width=40, show="*")
password_entry.grid(row=1, column=1, padx=(40, 10), sticky="e")

# Unlock Button
unlock_button = tk.Button(root, text="Unlock Vault", font=button_font, padx=20, pady=5)
unlock_button.grid(row=1, column=2, padx=(10, 40), sticky="w")

# Table Header Label (centered)
stored_header = tk.Label(root, text="Stored Credentials table", font=stored_header_font)
stored_header.grid(row=2, column=0, columnspan=3, pady=40, sticky="n")


# Header Row
headers = ["Website", "Username", "Password", "Copy", "Reveal"]
for col, header in enumerate(headers):
    tk.Label(root, text=header, font=header_font, borderwidth=2, relief="groove", padx=10, pady=5)\
        .grid(row=3, column=col, sticky="nsew")

def create_row(row_index, website, username, password_plain):
    masked_password = "*" * 10

    tk.Label(root, text=website, font=cell_font, borderwidth=1, relief="groove", padx=5, pady=5)\
      .grid(row=row_index, column=0, sticky="nsew")

    tk.Label(root, text=username, font=cell_font, borderwidth=1, relief="groove", padx=5, pady=5)\
      .grid(row=row_index, column=1, sticky="nsew")

    password_label = tk.Label(root, text=masked_password, font=cell_font, borderwidth=1, relief="groove", padx=5, pady=5)
    password_label.grid(row=row_index, column=2, sticky="nsew")

    # Copy function
    def copy_password():
        root.clipboard_clear()
        root.clipboard_append(password_plain)
        root.update()

    tk.Button(root, text="Copy", font=cell_font, command=copy_password)\
      .grid(row=row_index, column=3, sticky="nsew", padx=5, pady=5)

    # Toggle function (toggle password display)
    def toggle_password():
        if password_label.cget("text").startswith("*"):
            password_label.config(text=password_plain)
            reveal_button.config(text="Hide")
        else:
            password_label.config(text=masked_password)
            reveal_button.config(text="Show")

    reveal_button = tk.Button(root, text="Show", font=cell_font, command=toggle_password)
    reveal_button.grid(row=row_index, column=4, sticky="nsew", padx=5, pady=5)


# Create data rows
for idx, entry in enumerate(data, start=4):
    create_row(idx, entry["website"], entry["username"], entry["password"])

root.mainloop()
