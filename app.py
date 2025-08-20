import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

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
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_columnconfigure(2, weight=1)

        # Define fonts centrally
        self.font_header = ('Arial', 24, 'bold')
        self.font_label = ('Arial', 16, 'bold')
        self.font_entry = ('Arial', 16)

        self.password_labels = {}
        self.reveal_buttons = {}

    def main(self):
        """
        Build the UI components and start the Tkinter event loop.
        """
        self.header()
        self.master_password_section()
        self.run_main_event()

    def header(self):
        """
        Create and place the header label on the window.
        """
        header = tk.Label(self.root,
                          text='Password Manager',
                          font=self.font_header,
                          padx=15,
                          pady=15
                          )
        header.grid(row=0, column=0, columnspan=3, pady=(40, 20), sticky="")

    def master_password_section(self):
        """
        Create and place the master password input section:
        label, entry field, and unlock button.
        """
        self.password_label = tk.Label(self.root,
                                       text='Enter Master Password:',
                                       font=self.font_label)

        self.password_entry = tk.Entry(self.root,
                                       show='*',
                                       font=self.font_entry)

        self.unlock_button = tk.Button(self.root,
                                       text="Unlock Vault",
                                       command=self.unlock_vault)

        self.password_label.grid(row=1, column=0, padx=(20, 2), pady=10, sticky='e')
        self.password_entry.grid(row=1, column=1, padx=2, pady=10, sticky='ew')
        self.unlock_button.grid(row=1, column=2, padx=(2, 10), pady=10, sticky='w')

        self.password_entry.focus_set()

    def unlock_vault(self):
        """
        Callback for the 'Unlock Vault' button.
        Validates input and handles vault unlocking logic (to be implemented).
        """
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter your master password")
            return
        
        self.credentials_table_custom()

    def credentials_table_custom(self):
        self.headers = ['Website', 'Username', 'Password', 'Actions']

        self.table_container = tk.Frame(self.root, bd=2, relief='solid', width=800, height=300)
        self.table_container.grid(row=2, column=1, pady=40)

        self.generate_table_header()
        self.generate_table_data()

    def add_vertical_separator(self, col, row):
        if col < len(self.headers) - 1:
            v_separator = ttk.Separator(self.table_container, orient='vertical')
            v_separator.grid(row=row, column=col * 2 + 1, sticky='ns', pady=5)

    def generate_table_header(self):
        for col, header in enumerate(self.headers):
            header = tk.Label(self.table_container, text=header, font=self.font_label, bd=2)
            header.grid(row=0, column=col * 2, padx=10, sticky='')

            self.add_vertical_separator(col, 0)

    def generate_table_data(self):
        self.data = [
            {"website": "example.com", "username": "john_doe", "password": "MySecurePass123"},
            {"website": "gmail.com", "username": "jane123", "password": "Another$ecret"},
            {"website": "github.com", "username": "coder007", "password": "Code@2023"},
        ]
        for row_idx, row in enumerate(self.data, start=1):
            for col_index, key in enumerate(row):
                value = row[key]
                display_value = '******' if key == 'password' else value
                data_label = tk.Label(self.table_container,
                                      text=display_value,
                                      font=self.font_entry,
                                      anchor='w')
                data_label.grid(row=row_idx, column=col_index * 2, padx=10, pady=5, sticky='')
                if key == 'password':
                    self.password_labels[row_idx] = (data_label, value)
                self.add_vertical_separator(col_index, row_idx)
            self.add_reveal_button(row_idx)
            self.add_copy_button(row_idx)

    def add_reveal_button(self, row_idx):
        actions_start_col = len(self.headers) * 2
        self.reveal_button = ttk.Button(self.table_container,
                                        text="Show",
                                        cursor="hand2",
                                        command=lambda r=row_idx: self.toggle_password(r))
        self.reveal_button.grid(row=row_idx, column=actions_start_col, sticky="nsew", padx=5, pady=5)
        self.reveal_buttons[row_idx] = self.reveal_button

    def toggle_password(self, row_idx):
        label, actual_password = self.password_labels[row_idx]
        button = self.reveal_buttons[row_idx]

        if label.cget("text").startswith("*"):
            label.config(text=actual_password)
            button.config(text="Hide")
        else:
            label.config(text="******")
            button.config(text="Show")

    def add_copy_button(self, row_idx):
        actions_start_col = (len(self.headers) * 2) + 1
        button = ttk.Button(self.table_container,
                            text="Copy",
                            cursor="hand2",
                            command=lambda r=row_idx: self.copy_password(r))
        button.grid(row=row_idx, column=actions_start_col, sticky="nsew", padx=5, pady=5)

    def copy_password(self, row_idx):
        _, actual_password = self.password_labels[row_idx]
        self.root.clipboard_clear()
        self.root.clipboard_append(actual_password)
        self.root.update()
        messagebox.showinfo("Copied", "Password copied to clipboard")

    def run_main_event(self):
        """
        Start the Tkinter main event loop.
        """
        self.root.mainloop()


if __name__ == '__main__':
    manager = PasswordManager()
    manager.main()
