# s.py (Server)

import socket
import os

HOST = '127.0.0.1'
PORT = 8000

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def upload_file(connection, address):
    username_length = int.from_bytes(connection.recv(4), 'big')
    username = connection.recv(username_length)

    filename_length = int.from_bytes(connection.recv(4), 'big')
    filename = connection.recv(filename_length).decode('utf-8')

    file_data = b''
    while True:
        data = connection.recv(1024)
        if not data:
            break
        file_data += data

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, 'wb') as file:
        file.write(file_data)

    print(f"File received and saved: {filename} from {address}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        connection, address = server.accept()
        print(f"Connected to client: {address}")
        upload_file(connection, address)
        connection.close()

if __name__ == "__main__":
    main()
