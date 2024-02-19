import socket
import threading
import datetime

# ANSI escape code for red text
GREEN_TEXT = "\033[92m" #GREEN
RED_TEXT = "\033[91m"   # RED
RESET_TEXT = "\033[0m"  # DEFAULT
CYAN_TEXT = "\033[96m"  # CYAN

# List to store connected clients and their names
clients = {}
addresses = {}

# Server configuration
host = '127.0.0.1'
port = 12345

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))

# Function to handle client connections
def handle_client(client_socket, username):
    # Send a welcome message to the client
    #client_socket.send(f"Welcome, {username}! to the chat room\n".encode())
    
    timestamps_enabled = True  # Initialize timestamps state
    broadcast(f'{GREEN_TEXT}{username} joined the chat.{RESET_TEXT}')

    while True:
        try:
        
            message = client_socket.recv(1024).decode()
            if message:
                # Check for special commands
                if message.lower() == 'exit':
                    client_socket.send('Goodbye!'.encode())
                    del clients[username]
                    client_socket.close()
                    #broadcast(f'{username} left the chat.')
                    broadcast(f'{RED_TEXT}{username} left the chat.{RESET_TEXT}')
                    break
                elif message.lower() == 'listusers':
                    active_users = ', '.join(clients.keys())
                    client_socket.send(f'Active users: {active_users}\n'.encode())
                elif message.lower() == 'help':
                    client_socket.send(f"- 'exit' to leave\n- 'listusers' to see active users\n- 'timestamps' to toggle timestamps.\n".encode())
                elif message.lower() == 'timestamps':
                    timestamps_enabled = not timestamps_enabled  # Toggle timestamps on/off
                    if timestamps_enabled:
                        client_socket.send('Timestamps are now enabled.\n'.encode())
                    else:
                        client_socket.send('Timestamps are now disabled.\n'.encode())
                else:
                    if timestamps_enabled:
                        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                        timestamp_message = f'{CYAN_TEXT} [{timestamp}]{RESET_TEXT}'
                        message = f"{message} {timestamp_message}"
                    broadcast(f'{username}: {message}')

        except Exception as e:
            print(e)
            break

# Function to broadcast messages to all connected clients
def broadcast(message):
    for client_socket in clients.values():
        client_socket.send(message.encode())

# Main server loop
server_socket.listen(5)
print(f"Server listening on {host}:{port}")

while True:
    client_socket, client_addr = server_socket.accept()
    print(f"Accepted connection from {client_addr}")
    
    username = client_socket.recv(1024).decode()
    clients[username] = client_socket
    addresses[client_socket] = client_addr
    
    print(f"User {username} connected from {client_addr}")
    
    client_socket.send(f"Welcome, {username}! to the chat room\n".encode())
    
    # Create a thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, username))
    client_thread.start()
