import socket
import threading
import time
from Colors import Colors
from Configuration import Configuration
from Server.TCPHandler import TCPHandler
from Server.OfferBroadcaster import OfferBroadcaster
from Server.UDPHandler import UDPHandler


class Server:
    config = Configuration().get_config()

    def __init__(self, server_ip):

        self.server_ip = server_ip
        self.colors = Colors()

        #  TCP socket
        # create tcp socket
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # we want to reuse the address again
        #self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.tcp_socket.setsockopt(socket.SOL_SOCKET, 1)
        #bind the tcp socket to ip and port
        # we actually tell the OS to save the combination for our program and dont let any other process to use it
        self.tcp_socket.bind((self.server_ip, 0))

        #  UDP socket
        #create udp socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #we want to reuse the address again
        #self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        #bind udp socket to ip and port
        # we actually tell the OS to save the combination for our program and dont let any other process to use it
        self.udp_socket.bind((self.server_ip, 0))

        self.tcp_port = self.tcp_socket.getsockname()[1]
        self.udp_port = self.udp_socket.getsockname()[1]

    def start(self):
        """
        start the server activity
        """
        print(self.colors.SERVER_STATUS + f"Server started, listening on IP address {self.server_ip}" + self.colors.RESET)

        self.tcp_socket.listen(5)

        # start broadcast thread for sending offers to clients
        broadcast_offer = OfferBroadcaster(self.udp_socket,self.server_ip, self.udp_port, self.tcp_port)
        broadcast_thread = threading.Thread(target=broadcast_offer.broadcast)
        broadcast_thread.daemon = False
        broadcast_thread.start()


        # one handler process all incoming UDP packets no connections needed
        udp_handler = UDPHandler(self.udp_socket)
        udp_thread = threading.Thread(target=udp_handler.listen_for_requests)
        udp_thread.daemon = False
        udp_thread.start()

        while True:
            try:
                self._handle_tcp_connections()

            except Exception as e:
                print(self.colors.format_error(f"Error handling connections: {e}"))

    def _handle_tcp_connections(self):
        """Handles incoming TCP connections"""
        # waits for and accepts a new connection
        try:

            client_socket, addr = self.tcp_socket.accept()
            # update the user that the TCP connection succeeded
            print(self.colors.format_success_connection(f"New TCP connection from {addr}"))

            # open thread for each TCP connection and start them
            handler = TCPHandler(client_socket, addr)
            handler_thread = threading.Thread(target=handler.handle)
            handler_thread.daemon = False
            handler_thread.start()

        except Exception as e:
            print(e)


