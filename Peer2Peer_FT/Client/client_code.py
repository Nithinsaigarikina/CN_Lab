import os
import tkinter as tk
from tkinter import filedialog, messagebox
import socket
import threading

HOST = '127.0.0.1'
PORT = 4321

def send_file():
    username = username_entry.get()
    file_path = filedialog.askopenfilename()

    if not file_path:
        messagebox.showerror("Error", "No file selected.")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        print("Connected to server.")

        # Send username
        client_socket.sendall(len(username).to_bytes(4, 'big'))
        client_socket.sendall(username.encode())

        # Send filename
        filename = os.path.basename(file_path)
        client_socket.sendall(len(filename).to_bytes(4, 'big'))
        client_socket.sendall(filename.encode())

        # Send file data
        with open(file_path, 'rb') as file:
            file_data = file.read()
            client_socket.sendall(file_data)

        messagebox.showinfo("Success", "File uploaded successfully.")
        file_list.insert(tk.END, f"{username}: {filename}")  # Add to listbox
    except Exception as e:
        print(f"Error uploading file: {e}")
        messagebox.showerror("Error", "Error uploading file. Please try again later.")
    finally:
        client_socket.close()

def listen_for_messages_from_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.bind((HOST, PORT))
    client_socket.listen()

    while True:
        conn, addr = client_socket.accept()
        print(f"Connected by {addr}")

        # Receive username
        username_length = int.from_bytes(conn.recv(4), 'big')
        username = conn.recv(username_length).decode()

        # Receive filename
        filename_length = int.from_bytes(conn.recv(4), 'big')
        filename = conn.recv(filename_length).decode()

        with open(filename, 'wb') as file:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                file.write(data)
        
        messagebox.showinfo("New File", f"New file received: {filename} from {username}")
        file_list.insert(tk.END, f"{username}: {filename}")

def resize_image(event):
    global resized_image, original_image
    new_width = event.width
    new_height = event.height
    resized_image = original_image.resize((new_width, new_height))
    canvas.create_image(0, 0, anchor="nw", image=resized_image)

window = tk.Tk()
window.title("File Upload Client")
window.geometry("400x300")

canvas = tk.Canvas(window, width=400, height=300)
canvas.pack(fill="both", expand=True)

original_image = tk.PhotoImage(file="gradient.png")
resized_image = original_image  # Initial resized image is the same as original
canvas.create_image(0, 0, anchor="nw", image=resized_image)

canvas.bind("<Configure>", resize_image)

username_label = tk.Label(window, text="Username:", font=("Times New Roman", 12), bg="#6699ff", fg="white")
username_label.place(relx=0.3, rely=0.2, anchor="center")

username_entry = tk.Entry(window, font=("Times New Roman", 12))
username_entry.place(relx=0.7, rely=0.2, anchor="center")

file_button = tk.Button(window, text="Choose File", font=("Times New Roman", 12), command=send_file)
file_button.place(relx=0.5, rely=0.5, anchor="center")

# Create listbox for file info
file_list = tk.Listbox(window)
file_list.place(relx=0.5, rely=0.7, anchor="center")

# Start listening for messages from server in a separate thread
threading.Thread(target=listen_for_messages_from_server).start()

window.mainloop()
