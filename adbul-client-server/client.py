import socket
import threading

class PokerClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print("Connected to the server.")

        # Receive and print the welcome message
        welcome_msg = self.client_socket.recv(1024).decode()
        print(welcome_msg)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                print(message)
            except ConnectionResetError:
                print("Disconnected from the server.")
                break

    def send_message(self, message):
        self.client_socket.send(message.encode())

if __name__ == "__main__":
    client = PokerClient('localhost', 5555)
    client.connect()

    # Start a thread to receive messages from the server
    threading.Thread(target=client.receive_messages, daemon=True).start()

    while True:
        message = input("Your move: ")
        client.send_message(message)
