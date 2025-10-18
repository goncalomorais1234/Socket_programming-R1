#Server

from socket import *

SERVER_PORT = 12000
BUFFER = 2048
ENC = "utf-8"

def main():
    # create TCP
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # bind socket to local port number (12000) 
    serverSocket.bind(('', SERVER_PORT))

    # server begins listening for requests
    serverSocket.listen(1)
    print('The server is ready to receive on port', SERVER_PORT)

    while True:                       # loop forever
        # wait for client
        connectionSocket, addr = serverSocket.accept()
        print('Connected by', addr)

        try:
            # echo
            while True:
                data = connectionSocket.recv(BUFFER)   # bytes
                if not data:
                    break
                msg = data.decode(ENC).strip()

                if msg == '/quit':
                    connectionSocket.send(('*** bye ***\n').encode(ENC))
                    break

                # echo back 
                reply = (msg.upper() + '\n').encode(ENC)
                connectionSocket.send(reply)
        except:
            #for transient client errors
            pass
        finally:
            connectionSocket.close()
            print('Client disconnected')

if __name__ == "__main__":
    main()

