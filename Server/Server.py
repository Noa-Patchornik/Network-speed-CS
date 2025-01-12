import socket
import threading
from Colors import Colors
from Configuration import Configuration
from Server.TCPHandler import TCPHandler
from Server.OfferBroadcaster import OfferBroadcaster
from Server.UDPHandler import UDPHandler


class Server:
    config = Configuration().get_config()

    def __init__(self, server_ip, tcp_port, udp_port):

        self.server_ip = server_ip
        self.tcp_port = tcp_port
        self.udp_port = udp_port
        self.colors = Colors()

        #  TCP socket
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_socket.bind((self.server_ip, self.tcp_port))

        #  UDP socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udp_socket.bind((self.server_ip, self.udp_port))

    def start(self):
        """
        start the server activity
        """
        print(self.colors.SERVER_STATUS + f"Server started, listening on IP address {self.server_ip}"
              + self.colors.RESET)
        self.tcp_socket.listen(5)

        # start broadcast thread for sending offers to clients
        broadcast_offer = OfferBroadcaster(self.udp_socket)
        broadcast_thread = threading.Thread(target=broadcast_offer.broadcast)
        broadcast_thread.daemon = True
        broadcast_thread.start()

        # one handler process all incoming UDP packets no connections needed
        udp_handler = UDPHandler(self.udp_socket)
        udp_thread = threading.Thread(target=udp_handler.listen_for_requests)
        udp_thread.daemon = True
        udp_thread.start()

        while True:
            try:
                self._handle_tcp_connections()
            except Exception as e:
                print(self.colors.format_error(f"Error handling connections: {e}"))

    def _handle_tcp_connections(self):
        """Handles incoming TCP connections."""
        # waits for and accepts a new connection
        client_socket, addr = self.tcp_socket.accept()
        print(self.colors.format_success_connection(f"New TCP connection from {addr}") )

        # because each tcp needs a connection so it will be in a different thread
        handler = TCPHandler(client_socket, addr)
        handler_thread = threading.Thread(target=handler.handle)
        handler_thread.daemon = True
        handler_thread.start()
