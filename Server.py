import socket
import threading

# Define the server address (IP and port)
SERVER_IP = socket.gethostbyname(socket.gethostname())  # Grabs the user's local IP address
SERVER_PORT = 12345  # Change this to your server's port

# Create a socket to listen for incoming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()

# Function to broadcast messages to all connected clients
def broadcast(message, sender_socket):
    sender_address = sender_socket.getpeername()
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                # Include the sender's address in the message
                client_socket.send(f"{sender_address[0]}:{sender_address[1]}: {message}".encode('utf-8'))
            except:
                # Remove the client if there is an issue sending the message
                clients.remove(client_socket)
                client_socket.close()

# Function to handle client connections
def handle_client(client_socket):
    # Get the full client address, including port
    client_address = client_socket.getpeername()

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                # Remove the client if the connection is closed
                print(f"User {client_address[0]}, has disconnected.")
                clients.remove(client_socket)
                client_socket.close()
                break
            else:
                # Print the received message to the server's console
                print(f"Received message from {client_address[0]}:{client_address[1]}: {message.decode('utf-8')}")
                
                # Broadcast the received message to all clients
                broadcast(message.decode('utf-8'), client_socket)
        except:
            # Remove the client if there is an issue receiving messages
            print(f"User {client_address[0]}, has disconnected.")
            clients.remove(client_socket)
            client_socket.close()
            break

# Store client connections
clients = []

# Main server loop to accept incoming connections
print(f"Server is listening on {SERVER_IP}:{SERVER_PORT}")
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    
    # Add the client socket to the list of clients and start handling the client
    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()