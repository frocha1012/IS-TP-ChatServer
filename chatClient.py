import socket
import threading

COLORS = {
    'red': "\033[91m",
    'green': "\033[92m",
    'yellow': "\033[93m",
    'blue': "\033[94m",
    'purple': "\033[95m",
    'cyan': "\033[96m",
    'reset': "\033[0m"
}

# Client configuration
host = '127.0.0.1'
port = 12345

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Get user's name
username = input("Enter your name: ")
client_socket.send(username.encode())

# Function to receive and display messages from the server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            # An error occurred, likely the server closed the connection
            print("Disconnected from the server.")
            client_socket.close()
            break

# Function to send messages to the server
def send_messages():
    while True:
        message = input()
        client_socket.send(message.encode())
        clear_console_input()

def clear_console_input():
    print("\033[A                             \033[A")

    
# Create threads for sending and receiving messages
receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)

# Start the threads
receive_thread.start()
send_thread.start()

