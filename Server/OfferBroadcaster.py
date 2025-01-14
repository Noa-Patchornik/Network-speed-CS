import socket
import struct
import time

from Colors import Colors
from Configuration import Configuration


class OfferBroadcaster:
    def __init__(self, udp_socket, server_IP, udp_port, tcp_port):
        self.colors = Colors()
        self.config = Configuration().get_config()
        self.udp_socket = udp_socket
        self.server_IP = server_IP
        self.udp_port = udp_port
        self.tcp_port = tcp_port

    def broadcast(self):
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            try:
                message = self.creat_offer_request()
                # Send to broadcast port that client listens on
                self.udp_socket.sendto(message, ('<broadcast>', self.config.broadcast_port))
                print(f"Sent offer with UDP port {self.udp_port} and TCP port {self.tcp_port}")
                time.sleep(1)
            except Exception as e:
                print(self.colors.format_error(f"Error broadcasting offer: {e}\n"))

    def creat_offer_request(self):
        return struct.pack('!IBHH',
                          self.config.cookie,
                          self.config.offer_message_type,
                          self.udp_port,  # Dynamic UDP port
                          self.tcp_port)  # Dynamic TCP port