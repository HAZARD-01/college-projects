import socket
import threading
import tkinter as tk

def send_message():
    message = entry.get()
    client_socket.send(message.encode('utf-8'))
    entry.delete(0, tk.END)

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(f"Received message: {message}")
            messages_listbox.insert(tk.END, message)
        except ConnectionResetError:
            print("Server disconnected.")
            break

def on_closing():
    client_socket.close()
    root.destroy()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    print("Attempting to connect to the server...")
    client_socket.connect(('127.0.0.1', 12345))  
    print("Connection established.")
except ConnectionRefusedError:
    print("Error: Unable to connect to the server. Make sure the server is running.")
    exit()

root = tk.Tk()
root.title("Chat App")

entry = tk.Entry(root)
entry.pack(pady=10)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

messages_listbox = tk.Listbox(root, height=15, width=50)
messages_listbox.pack(pady=20)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
