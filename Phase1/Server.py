import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

clients = {}

class ServerUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Messenger Server")

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=10)

def broadcast_message(message, sender_socket=None):
    for client_socket, username in clients.items():
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except:
                pass

def handle_client(client_socket, client_address, server_ui):
    username = client_socket.recv(1024).decode()
    clients[client_socket] = username

    welcome_message = f"[+] Welcome, {username}! You've joined the chat."
    server_ui.text_area.insert(tk.END, welcome_message + f" ({client_address[0]}:{client_address[1]})\n")
    client_socket.send(welcome_message.encode())

    broadcast_message(f"Response from {username}: {welcome_message}", client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message.lower() == '/logout':
                server_ui.text_area.insert(tk.END, f"[-] {username} has left the chat.\n")
                broadcast_message(f"[-] {username} has left the chat.")
                del clients[client_socket]
                client_socket.close()
                break
            else:
                server_ui.text_area.insert(tk.END, f"Message from {username}: {message}\n")
                broadcast_message(f"Message from {username}: {message}", client_socket)
        except:
            # Handle disconnection here if needed
            break

def start_server(server_ui):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)

    server_ui.text_area.insert(tk.END, "[+] Server started.\n[+] Waiting for clients to connect...\n")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, server_ui))
        client_thread.start()

def main():
    root = tk.Tk()
    server_ui = ServerUI(root)
    server_thread = threading.Thread(target=start_server, args=(server_ui,))
    server_thread.start()
    root.mainloop()

if __name__ == "__main__":
    main()