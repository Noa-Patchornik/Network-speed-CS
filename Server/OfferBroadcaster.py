import socket
import struct
import time
from colorama import Fore

from Colors import Colors
from Configuration import Configuration


class OfferBroadcaster:
    def __init__(self, udp_socket):
        # add support in colorful console as requested
        self.colors = Colors()
        # using configuration file to avoid hard coding definitions
        self.config = Configuration().get_config()
        self.udp_socket = udp_socket

    def broadcast(self):
        """Broadcasts offer messages every second."""
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        while True:
            try:
                # create offer message according to protocol
                message = self.construct_offer_request()
                # send it to all client in broadcast form which means = send to all devices on the local network
                self.udp_socket.sendto(message, ('<broadcast>', self.config.udp_port))
                # don't do it so fast
                time.sleep(1)
            except Exception as e:
                print(self.colors.format_error(f"Error broadcasting offer: {e}\n"))

    def construct_offer_request(self):
        """
        constructing offering messages from server to client
        """
        message = struct.pack('!IBHH',
                              self.config.cookie,
                              self.config.offer_message_type,
                              self.config.udp_port,
                              self.config.tcp_port
                              )
        return message
