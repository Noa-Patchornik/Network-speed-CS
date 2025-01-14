import socket
import threading
from Configuration import Configuration
from Client.Client import Client
from Server.Server import Server
import time


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()


def start_server():
    # Starting the server side, using configuration file to easily change what we need
    server_ip = get_ip()
    print(server_ip)
    #creat the server object and start it
    server = Server(server_ip)
    server.start()


def start_client():
    # creating a Client object and starting it
    client = Client()
    client.start()


def main():
    #Start the server in a separate thread
    # server_thread = threading.Thread(target=start_server)
    # server_thread.daemon = True
    # server_thread.start()
    # # set the server thread to sleep to creat the client
    time.sleep(1)


    start_client()


if __name__ == "__main__":
    main()