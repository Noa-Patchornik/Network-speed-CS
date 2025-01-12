from colorama import Fore

from Client.ClientHandler import ClientHandler
from Client.Listener import Listener
from Colors import Colors
from Configuration import Configuration


class Client:
    def __init__(self):
        # using configuration file to avoid hard coding definitions
        self.config = Configuration().get_config()
        # crate a listener for offer suggestions from servers
        self.listener = Listener()
        # handle server suggestions
        self.handler = ClientHandler()
        # add support in colorful console as requested
        self.colors = Colors()

    def get_user_input(self):
        """
        gets user input as requested in the file
        """
        while True:
            try:
                #asking details from user
                file_size = int(input(f"{self.colors.USER_INPUT}Enter file size (bytes): {self.colors.RESET}\n"))
                tcp_count = int(input(f"{self.colors.USER_INPUT}Enter number of TCP connections: {self.colors.RESET}\n"))
                udp_count = int(input(f"{self.colors.USER_INPUT}Enter number of UDP connections: {self.colors.RESET}\n"))
                # validation of input user
                if file_size <= 0 or tcp_count < 0 or udp_count < 0:
                    raise ValueError

                return file_size, tcp_count, udp_count

            except ValueError:
                print(self.colors.format_error("Please enter valid positive numbers\n"+ self.colors.RESET))

    def start(self):
        """
        start the client(asking for details, listen for offers and transfer requests and get payload
        """

        # ask user for details
        file_size, tcp_count, udp_count = self.get_user_input()
        while True:
            print(self.colors.CLIENT_STATUS + "Client started, listening for offer requests...\n" + self.colors.RESET)
            # transfer operations
            try:
                # listen from offers from servers
                server_info = self.listener.listen_for_offer()
                # in case of getting an offer correctly
                if server_info:
                    # transfer the data
                    self.handler.handle_transfers(server_info, file_size, tcp_count, udp_count)
                    # when finished print iin for logging robust and continue to ask details from user again
                    print(self.colors.format_success("All transfers complete, listening for offer requests"))
            # in case of failure in transfer
            except Exception as e:
                print(self.colors.format_error(f"Error during transfer: {e}\n"+ self.colors.RESET))

