# Server Handler.py (TCP)
import time

from Colors import Colors
from Configuration import Configuration


class TCPHandler:
    """
    manages TCP connections on the server side
    """

    def __init__(self, client_socket, addr):
        # for colored console output
        self.colors = Colors()
        #  connected clients socket
        self.client_socket = client_socket
        # clients address (IP, port)
        self.addr = addr
        # using configuration file to avoid hard coding definitions
        self.config = Configuration().get_config()

    def handle(self):
        """
        handling the requested - payload sending
        """
        try:
            # received file size request from client
            self.client_socket.settimeout(30)
            size_str = self.client_socket.recv(1024).decode().strip()
            file_size = int(size_str)

            print(self.colors.TCP_TRANSFER + "Starting TCP file transfer...\n" + self.colors.RESET)

            # Send entire file at once
            data = self.config.dummy_bit * file_size
            self.client_socket.send(data)

            print(self.colors.TCP_TRANSFER + f"TCP transfer complete for {self.addr}\n" + self.colors.RESET)
        except Exception as e:
            print(self.colors.format_error(f"Error handling client {self.addr}: {e}\n"))
        finally:
            time.sleep(0.5)
            self.client_socket.close()
