import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json

class PasswordManager:
    """
    A simple offline password manager GUI using Tkinter.

    This application allows the user to enter a master password to unlock
    the encrypted vault (logic to be implemented). It features a header,
    password input, and unlock button.

    Attributes:
        root (tk.Tk): The main Tkinter window.
        font_header (tuple): Font for the header label.
        font_label (tuple): Font for labels.
        font_entry (tuple): Font for entry widgets.
        password_label (tk.Label): Label for master password input.
        password_entry (tk.Entry): Entry widget to input the master password.
        unlock_button (tk.Button): Button to unlock the vault.
    """

    def __init__(self):
        """
        Initialize the main window, configure grid and fonts.
        """
        self.root = tk.Tk()
        self.root.geometry("1200x800")
        self.root.title("Password Manager")
        self.root.minsize(600, 400)

        # Configure grid columns to manage resizing
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)


        # Define fonts centrally
        self.font_header = ('Segoe UI', 28, 'bold')
        self.font_label = ('Segoe UI', 14, 'bold')
        self.font_entry = ('Segoe UI', 14)


        self.password_labels = {}
        self.reveal_buttons = {}
        self.filename = 'vault.dat'

    def main(self):
        """
        Build the UI components and start the Tkinter event loop.
        """
        self.header()
        self.add_new_section()
        self.master_password_section()
        self.run_main_event()

    def header(self):
        """
        Create and place the header label on the window.
        """
        header = tk.Label(
            self.root,
            text='🔐 Password Manager',
            font=self.font_header,
            bg="#2c3e50",
            fg="#ecf0f1",
            pady=20
        )
        header.grid(row=0, column=0, columnspan=3, sticky='ew')

    def master_password_section(self):
        """
        Create and place the master password input section:
        label, entry field, and unlock button.
        """
        password_frame = tk.Frame(self.root)
        password_frame.grid(row=1, column=0, columnspan=3, pady=20)

        label = tk.Label(password_frame, text="Enter Master Password:", font=self.font_label)
        label.pack(side='left', padx=(0, 10))

        self.password_entry = tk.Entry(password_frame, show='*', font=self.font_entry, width=30)
        self.password_entry.pack(side='left')

        self.unlock_button = tk.Button(password_frame, text="Unlock Vault", font=self.font_entry, command=self.unlock_vault)
        self.unlock_button.pack(side='left', padx=10)

    def unlock_vault(self):
        """
        Callback for the 'Unlock Vault' button.
        Validates input and handles vault unlocking logic (to be implemented).
        """
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter your master password")
            return
        
        if self.read_vault_data():
            self.credentials_table_custom()

    def read_vault_data(self):
        try:
            with open(self.filename, "r") as file:
                self.data = json.load(file)
                return True
        except FileNotFoundError:
            messagebox.showerror("Error", f"Error: {self.filename} file not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"Error: Failed to decode JSON from {self.filename}.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        return False

    def credentials_table_custom(self):
        headers = ['Website', 'Username', 'Password', 'Actions']
        
        # Container for the table
        self.table_frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief='groove')
        self.table_frame.grid(row=3, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")

        # Table header
        for col, header in enumerate(headers):
            label = tk.Label(self.table_frame, text=header, font=self.font_label, bg="#f0f0f0")
            label.grid(row=0, column=col, sticky='nsew')

        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(1, weight=1)
        self.table_frame.grid_columnconfigure(2, weight=1)
        self.table_frame.grid_columnconfigure(3, weight=1)

        # Table data
        self.password_labels = {}
        print(len(self.data))
        for idx, entry in enumerate(self.data, start=1):
            bg_color = "#ffffff"

            website = tk.Label(self.table_frame, text=entry['website'], font=self.font_entry, bg=bg_color)
            username = tk.Label(self.table_frame, text=entry['username'], font=self.font_entry, bg=bg_color)
            password_label = tk.Label(self.table_frame, text="******", font=self.font_entry, bg=bg_color)

            website.grid(row=idx, column=0, sticky='nsew')
            username.grid(row=idx, column=1, sticky='nsew')
            password_label.grid(row=idx, column=2, sticky='nsew')

            # Save reference for toggling
            self.password_labels[idx] = (password_label, entry['password'])

            # Action buttons
            action_frame = tk.Frame(self.table_frame, bg=bg_color)
            action_frame.grid(row=idx, column=3, pady=1)

            edit_btn = ttk.Button(action_frame, text="Edit", width=8, command=lambda i=idx: self.copy_password(i))
            reveal_btn = ttk.Button(action_frame, text="Reveal", width=8, command=lambda i=idx: self.toggle_password(i))
            copy_btn = ttk.Button(action_frame, text="Copy", width=8, command=lambda i=idx: self.copy_password(i))

            edit_btn.pack(side="left", padx=2)
            reveal_btn.pack(side="left", padx=2)
            copy_btn.pack(side="left", padx=2)

    def toggle_password(self, row_idx):
        label, actual_password = self.password_labels[row_idx]
        current_text = label.cget("text")
        if current_text == "******":
            label.config(text=actual_password)
        else:
            label.config(text="******")

    def copy_password(self, row_idx):
        _, actual_password = self.password_labels[row_idx]
        self.root.clipboard_clear()
        self.root.clipboard_append(actual_password)
        self.root.update()
        messagebox.showinfo("Copied", "Password copied to clipboard.")

    def add_new_section(self):
        # Create a frame to hold the buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=2, column=0, columnspan=3, pady=10)

        # "Add New Entry" button
        self.add_link = tk.Button(self.button_frame,
                                  text="[+] Add New Entry",
                                  font=self.font_entry,
                                  command=self.unlock_vault)
        self.add_link.pack(side='left', padx=20)

        # "Exit" button
        self.exit_link = tk.Button(self.button_frame,
                                   text="Exit",
                                   font=self.font_entry,
                                   command=self.root.quit)
        self.exit_link.pack(side='left', padx=10)


    def run_main_event(self):
        """
        Start the Tkinter main event loop.
        """
        self.root.mainloop()


if __name__ == '__main__':
    manager = PasswordManager()
    manager.main()
