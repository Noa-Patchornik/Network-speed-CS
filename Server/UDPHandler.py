import struct
import threading
import time
from Colors import Colors
from Configuration import Configuration
from Server.PayloadSender import PayloadSender

""" Class that handle the UDP requests, valid the messages and send the required file to the client """
class UDPHandler:
    def __init__(self, udp_socket):
        self.udp_socket = udp_socket
        # add support in colorful console as requested
        self.colors = Colors()
        # using configuration file to avoid hard coding definitions
        self.config = Configuration().get_config()
        self.payload_sender = PayloadSender()

    def listen_for_requests(self):
        """Continuously listen for UDP requests from the clients"""

        while True:
            print(f"{self.colors.UDP_TRANSFER}UDP Handler started, listening for requests...\n" + self.colors.RESET)

            try:
                # receive the data from the client
                data, client_addr = self.udp_socket.recvfrom(1024)
                 # check if it is valid request
                if self.valid_request_msg(data):
                        print(self.colors.format_success_connection(f"Valid UDP request from {client_addr}"))
                        # Handle in separate thread
                        handler_thread = threading.Thread(
                            target=self.handle_request,
                            args=(data, client_addr) )
                        handler_thread.daemon = True
                        handler_thread.start()
            except Exception as e:
                print(self.colors.format_error(f"Error in UDP listener: {e}"))
                continue

    def handle_request(self, data, client_addr):
        """
        handle request msg from client and send data to client
        """
        try:
            #unpacking the data
            cookie, msg_type, file_size = struct.unpack('!IBQ', data)
            print(self.colors.UDP_TRANSFER + f"Starting UDP transfer of {file_size} bytes to {client_addr}\n" + self.colors.RESET)
            # sending it through UDP using the payload class
            self.payload_sender.send_file_udp(self.udp_socket, client_addr, file_size)
        except Exception as e:
            self.colors.format_error(e)

    def valid_request_msg(self,data):
        """
        validate the request msg
        """
        if len(data) == self.config.request_len:
            cookie, msg_type, file_size = struct.unpack('!IBQ', data)
            if cookie == self.config.cookie and msg_type == self.config.request_message_type:
                return True
        return False