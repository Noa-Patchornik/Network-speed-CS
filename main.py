import threading
from Configuration import Configuration
from Client.Client import Client
from Server.Server import Server


def start_server():
    config = Configuration().get_config()
    server_ip = config.server_ip
    tcp_port = config.tcp_port
    udp_port = config.udp_port

    server = Server(server_ip, tcp_port, udp_port)
    server.start()


def start_client():
    client = Client()
    client.start()


def main():
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    import time
    time.sleep(1)

    start_client()


if __name__ == "__main__":
    main()