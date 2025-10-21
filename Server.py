#Written by Goncalo Morais (ID:200695080) and Cagri Isilak (ID:210764050)

#Server file
import socket
import datetime
import threading

# Global variables
client_counter = 0
client_cache = {}
max_clients = 3
files_repo = {
    "file1.txt": "This is the content of file 1. Hello from server!",
    "file2.txt": "This is the content of file 2. Welcome to the chat application!"
}

def handle_client(client_socket, addr):
    global client_counter, client_cache
    
    # Assign client name
    client_counter += 1
    client_name = f"Client{client_counter:02d}"
    
    # Add to cache
    client_cache[client_name] = [{
        "address": list(addr),
        "connected_at": str(datetime.datetime.now()),
        "disconnected_at": None
    }]
    
    # Send client name to client
    client_socket.send(client_name.encode())
    
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
                
            print(f"Received from {client_name}: {data}")
            
            if data.lower() == "exit":
                # Update disconnect time in cache
                for entry in client_cache[client_name]:
                    if entry["disconnected_at"] is None:
                        entry["disconnected_at"] = str(datetime.datetime.now())
                break
            elif data.lower() == "status":
                response = str(client_cache)
                client_socket.send(response.encode())
            elif data.lower() == "list":
                file_list = ", ".join(files_repo.keys())
                client_socket.send(file_list.encode())
            elif data.lower() in [f.lower() for f in files_repo.keys()]:
                # Find the correct case for the filename
                actual_filename = next(f for f in files_repo.keys() if f.lower() == data.lower())
                file_content = files_repo[actual_filename]
                client_socket.send(file_content.encode())
            else:
                response = data + " ACK"
                client_socket.send(response.encode())
                
    finally:
        client_socket.close()

def start_server():
    global client_counter, client_cache
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
    server_socket.listen(5)
    print("Server is listening...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        
        # Check if we can accept more clients
        current_clients = sum(1 for client_entries in client_cache.values() 
                            for entry in client_entries 
                            if entry["disconnected_at"] is None)
        
        if current_clients >= max_clients:
            client_socket.send("Server is full. Please try again later.".encode())
            client_socket.close()
            continue
            
        # Handle client in a new thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.daemon = True
        client_thread.start()

if __name__ == '__main__':
    start_server()