import struct
import threading
import time

from Colors import Colors
from Configuration import Configuration
from Server.PayloadSender import PayloadSender


class UDPHandler:
    def __init__(self, udp_socket):
        self.udp_socket = udp_socket
        # add support in colorful console as requested
        self.colors = Colors()
        # using configuration file to avoid hard coding definitions
        self.config = Configuration().get_config()
        self.payload_sender = PayloadSender()

    def listen_for_requests(self):
        """Continuously listen for UDP requests"""
        print("UDP Handler started, listening for requests...")
        while True:
            try:
                data, client_addr = self.udp_socket.recvfrom(1024)
                 # Valid request
                if self.valid_request_msg(data):
                        print(self.colors.UDP_TRANSFER + f"Valid UDP request from {client_addr}\n" + self.colors.RESET)
                        # Handle in separate thread
                        handler_thread = threading.Thread(
                            target=self.handle_request,
                            args=(data, client_addr)
                        )
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
            cookie, msg_type, file_size = struct.unpack('!IBQ', data)
            print(
                self.colors.UDP_TRANSFER + f"Starting UDP transfer of {file_size} bytes to {client_addr}\n" + self.colors.RESET)

            buffer_size = self.config.buffer_size
            total_segments = (file_size + buffer_size - 1) // buffer_size

            for segment_num in range(total_segments):
                packet = self.payload_sender.construct_payload_msg(total_segments, segment_num)
                self.udp_socket.sendto(packet, client_addr)
                if segment_num % 100 == 0:
                    print(
                        self.colors.SERVER_STATUS + f"Sent segment {segment_num + 1}/{total_segments}\n" + self.colors.RESET)

                time.sleep(0.001)  # Small delay to prevent flooding
        except Exception as e:
            self.colors.format_error((e))

    def valid_request_msg(self,data):
        """
        validate the request msg
        """
        if len(data) == self.config.request_len:
            cookie, msg_type, file_size = struct.unpack('!IBQ', data)
            if cookie == self.config.cookie and msg_type == self.config.request_message_type:
                return True
        return False