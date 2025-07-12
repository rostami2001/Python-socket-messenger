# client.py
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog
from tkinter import ttk  # Import ttk for themed widgets

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

class ClientUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Messenger Client")

        # Themed widget style
        style = ttk.Style()
        style.configure("TFrame", background="#333")
        style.configure("TButton", background="#4CAF50", foreground="white")
        style.configure("TLabel", background="#333", foreground="white")
        style.map("TButton", background=[('active', '#45a049')])

        self.frame = ttk.Frame(master, style="TFrame")
        self.frame.grid(column=0, row=0, padx=10, pady=10)

        self.text_area = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, bg="#444", fg="white")
        self.text_area.grid(column=0, row=0, padx=10, pady=10)

        self.entry = ttk.Entry(self.frame)
        self.entry.grid(column=0, row=1, padx=10, pady=10)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.grid(column=0, row=2, pady=10)

        self.username = simpledialog.askstring("Username", "Enter your username:")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_HOST, SERVER_PORT))
        self.client_socket.send(self.username.encode())

        self.recipient_username = simpledialog.askstring("Recipient Username", "Enter recipient username:")
        self.client_socket.send(self.recipient_username.encode())

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def send_message(self):
        message = self.entry.get()
        if message:
            self.client_socket.send(message.encode())
            self.entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                response = self.client_socket.recv(1024).decode()
                if not response:
                    self.text_area.insert(tk.END, "Disconnected from the server.\n")
                    break

                if response == "Recipient is not online.":
                    print(response)
                    break
                else:
                    self.text_area.insert(tk.END, f" {self.recipient_username}: {response}\n")
            except Exception as e:
                print(e)
                self.text_area.insert(tk.END, "Disconnected from the server.\n")
                break

def main():
    root = tk.Tk()
    client_ui = ClientUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()