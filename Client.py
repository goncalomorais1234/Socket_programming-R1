#Client
from socket import *

SERVER_NAME = 'localhost' 
SERVER_PORT = 12000
BUFFER = 2048
ENC = "utf-8"

def main():
    # create TCP socket and connect
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((SERVER_NAME, SERVER_PORT))

    try:
        while True:
            sentence = input("Input message (or /quit): ")
            clientSocket.send((sentence + "\n").encode(ENC))
            if sentence.strip() == "/quit":
                break

            modifiedSentence = clientSocket.recv(BUFFER)
            if not modifiedSentence:
                print("*** Server closed connection ***")
                break
            print("From Server:", modifiedSentence.decode(ENC).strip())
    finally:
        clientSocket.close()

if __name__ == "__main__":
    main()