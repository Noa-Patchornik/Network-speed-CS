import socket
import struct
from Colors import Colors
from Configuration import Configuration


class Listener:
    def __init__(self):
        # add support in colorful console as requested
        self.colors = Colors()
        # using configuration file to avoid hard coding definitions
        self.config = Configuration().get_config()

    def listen_for_offer(self):
        """ listens for all offer messages from servers """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # use the same port
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            s.bind(('', self.config.udp_port))

            while True:
                try:
                    # receive data from server
                    data, addr = s.recvfrom(self.config.buffer_size)
                    # validate the offer msg, if correctly constructed - return it for sending request later on
                    if len(data) == self.config.offer_len:
                        cookie, msg_type, udp_port, tcp_port = struct.unpack('!IBHH', data)
                        if (cookie == self.config.cookie and
                                msg_type == self.config.offer_message_type):
                            print(self.colors.CLIENT_STATUS + f"Received offer from {addr[0]}\n" + self.colors.RESET)
                            return addr[0], udp_port, tcp_port
                    else:
                        print(self.colors.format_error(
                            f"Received invalid offer, expected 9 bytes, got {len(data)} bytes.\n"+ self.colors.RESET))
                # in case of errors do:
                except socket.timeout:
                    continue
                except Exception as e:
                    print(self.colors.format_error(f"Error receiving offer: {e}\n"+ self.colors.RESET))
