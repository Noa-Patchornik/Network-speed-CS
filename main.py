import threading
from Configuration import Configuration
from Client.Client import Client
from Server.Server import Server
import time

def start_server():
    # Starting the server side, using configuration file to easily change what we need
    config = Configuration().get_config()
    server_ip = config.server_ip
    tcp_port = config.tcp_port
    udp_port = config.udp_port
    #creat the server object and start it
    server = Server(server_ip, tcp_port, udp_port)
    server.start()


def start_client():
    # creating a Client object and starting it
    client = Client()
    client.start()


def main():
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    # set the server thread to sleep to creat the client
    time.sleep(1)

    start_client()


if __name__ == "__main__":
    main()