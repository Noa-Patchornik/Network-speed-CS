# Server Handler.py (TCP)
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
            size_str = self.client_socket.recv(1024).decode().strip()
            file_size = int(size_str)

            print(self.colors.TCP_TRANSFER + "Starting TCP file transfer...\n" + self.colors.RESET)

            buffer_size = self.config.buffer_size
            remaining = file_size
            # the data itself doesn't matter so use the byte define in the config file
            dummy_chunk = self.config.dummy_bit * buffer_size

            # sending in chinks in order not to exceed the buffer size
            while remaining > 0:
                chunk_size = min(buffer_size, remaining)
                if chunk_size == buffer_size:
                    self.client_socket.send(dummy_chunk)
                else:
                    self.client_socket.send(self.config.dummy_bit * chunk_size)
                remaining -= chunk_size

            print(self.colors.TCP_TRANSFER + f"TCP transfer complete for {self.addr}\n" + self.colors.RESET)
        except Exception as e:
            print(self.colors.format_error(f"Error handling client {self.addr}: {e}\n"))
        finally:
            self.client_socket.close()
