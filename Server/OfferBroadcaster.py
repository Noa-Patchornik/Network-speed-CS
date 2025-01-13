import socket
import struct
import time
from Colors import Colors
from Configuration import Configuration
import netifaces

""" Class that is responsible to broadcast offers to the client saying that the server is offering its services"""
class OfferBroadcaster:
    def __init__(self, udp_socket,server_IP):
        # add support in colorful console as requested
        self.colors = Colors()
        # using configuration file to avoid hard coding definitions
        self.config = Configuration().get_config()
        self.udp_socket = udp_socket
        self.server_IP = server_IP

    def broadcast(self):
        """Broadcasts offer messages every second."""
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # The loop will work until a client will accept the offer
        while True:
            try:
                # create offer message according to protocol
                message = self.creat_offer_request()
                # send it to all client in broadcast form which means send to all devices on the local network
                self.udp_socket.sendto(message, ('<broadcast>', self.config.udp_port))
                # send offer every second
                print(f"{self.colors.SERVER_STATUS} Sent offer\n"+self.colors.RESET)
                time.sleep(1)
            except Exception as e:
                print(self.colors.format_error(f"Error broadcasting offer: {e}\n"))

    def creat_offer_request(self):
        """
        creat offer messages from server to client using the requested structure
        """
        message = struct.pack('!IBHH',
                              self.config.cookie,
                              self.config.offer_message_type,
                              self.config.udp_port,
                              self.config.tcp_port)
        return message

    def get_broadcast_address(self):


        # Get the network interfaces
        for interface in netifaces.interfaces():
            # Get the addresses associated with the interface
            addresses = netifaces.ifaddresses(interface)

            # Check if the interface has an IPv4 address
            if netifaces.AF_INET in addresses:
                for addr in addresses[netifaces.AF_INET]:
                    ip = addr['addr']
                    netmask = addr['netmask']
                    # Match the local IP address to find the corresponding interface
                    if ip == self.server_IP:
                        # Calculate the broadcast address
                        ip_binary = struct.unpack('>I', socket.inet_aton(ip))[0]
                        mask_binary = struct.unpack('>I', socket.inet_aton(netmask))[0]
                        broadcast_binary = ip_binary | ~mask_binary
                        return socket.inet_ntoa(struct.pack('>I', broadcast_binary & 0xFFFFFFFF))

        return None