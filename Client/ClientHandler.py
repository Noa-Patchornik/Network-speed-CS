import threading
from colorama import Fore

from Client.RequestTransfer import RequestTransfer
from Configuration import Configuration


class ClientHandler:
    def __init__(self):
        # using configuration file to avoid hard coding definitions
        self.config = Configuration().get_config()
        # create an instance of class that responsible for request msg creation and transfer it to server
        self.transfer = RequestTransfer()

    def handle_transfers(self, server_info, file_size, tcp_count, udp_count):
        """handles all transfers types (udp or tcp) each in a new thread for parallelism as requested"""
        # threads list
        threads = []
        #extracting details for transfer
        server_ip, udp_port, tcp_port = server_info

        # create tcp transfer
        for i in range(tcp_count):
            t = threading.Thread(
                target=self.transfer.tcp_transfer,
                args=(server_ip, tcp_port, file_size, i + 1)
            )
            threads.append(t)
            t.start()

        # create udp transfers
        for i in range(udp_count):
            t = threading.Thread(
                target=self.transfer.udp_transfer,
                args=(server_ip, udp_port, file_size, i + 1)
            )
            threads.append(t)
            t.start()

        # dont close untill all the threads finished
        for t in threads:
            t.join()
