# chat_client.py
import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")

        self.chat_window = scrolledtext.ScrolledText(root, state='disabled')
        self.chat_window.pack(padx=10, pady=10, fill='both', expand=True)

        self.entry = tk.Entry(root)
        self.entry.pack(padx=10, pady=10, fill='x', side='left', expand=True)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=10, side='right')

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 12345))

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def send_message(self, event=None):
        message = self.entry.get()
        if message:
            self.client_socket.send(message.encode('utf-8'))
            self.entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.chat_window.configure(state='normal')
                    self.chat_window.insert(tk.END, message + '\n')
                    self.chat_window.configure(state='disabled')
                    self.chat_window.yview(tk.END)
            except:
                break

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
