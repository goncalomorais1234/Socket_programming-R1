#Written by Goncalo Morais (ID:200695080) and Cagri Isilak (ID:210764050)

#Client File
import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))  # Connect to the server

    # Receive client name from server
    client_name = client_socket.recv(1024).decode()
    print(f"You are {client_name}")
    
    while True:
        message = input("Enter message: ")
        client_socket.send(message.encode())
        
        if message.lower() == "exit":
            break
            
        data = client_socket.recv(1024).decode()
        print(f"Server response: {data}")

    client_socket.close()

if __name__ == '__main__':
    start_client()