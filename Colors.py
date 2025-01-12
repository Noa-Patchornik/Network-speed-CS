
from colorama import Fore, Back, Style
import colorama

colorama.init()


class Colors:

    def __init__(self):
        # Server status
        self.SERVER_STATUS = Fore.BLUE + Style.BRIGHT
        # Client status
        self.CLIENT_STATUS = Fore.MAGENTA + Style.BRIGHT
        # User Input
        self.USER_INPUT = Back.BLACK + Fore.CYAN + Style.BRIGHT

        # Transfer status
        self.TCP_TRANSFER = Fore.LIGHTGREEN_EX
        self.UDP_TRANSFER = Fore.LIGHTCYAN_EX

        # Reset
        self.RESET = Style.RESET_ALL

    @staticmethod
    # Function for errors through all the project to maintain consistent design
    def format_error(message):
        return f"{Fore.RED}{message}{Style.RESET_ALL}"

    @staticmethod
    # Function for successful events
    def format_success(message):
        return f"{Back.BLACK}{message}{Style.RESET_ALL}\n"

    @staticmethod
    # Function for successful creating connection (UDP and TCP)
    def format_success_connection(message):
        return f"{Back.WHITE+Fore.BLACK}{message}{Style.RESET_ALL}\n"

    @staticmethod
    # Function that prints all the data about the TCP connection and the duration of it and the speed
    def format_tcp_transfer(transfer_num, duration, speed):
        return (f"{Fore.LIGHTGREEN_EX}TCP transfer #{Fore.BLACK + Back.GREEN}{transfer_num}{Style.RESET_ALL}{Fore.LIGHTGREEN_EX}, "
                f"total time: {Fore.BLACK + Back.GREEN}{duration:.2f}{Style.RESET_ALL}{Fore.LIGHTGREEN_EX} seconds, "
                f"total speed: {Fore.BLACK + Back.GREEN}{speed:.1f}{Style.RESET_ALL}{Fore.LIGHTGREEN_EX} bits/second{Style.RESET_ALL}\n")

    @staticmethod
    # Function that prints all the data about the UDP connection, the duration of it and the speed,
    # the amount of data that already received in the client side
    def format_udp_transfer(transfer_num, duration, speed, success_rate):
        return (f"{Fore.LIGHTCYAN_EX}UDP transfer #{Back.LIGHTCYAN_EX +Fore.BLACK}{transfer_num}{Style.RESET_ALL}{Fore.LIGHTCYAN_EX} finished, "
                f"total time: {Back.LIGHTCYAN_EX +Fore.BLACK}{duration:.2f}{Style.RESET_ALL}{Fore.LIGHTCYAN_EX} seconds, "
                f"total speed: {Back.LIGHTCYAN_EX +Fore.BLACK}{speed:.1f}{Style.RESET_ALL}{Fore.LIGHTCYAN_EX} bits/second, "
                f"percentage of packets received successfully: {Back.LIGHTCYAN_EX +Fore.BLACK}{success_rate:.0f}%{Style.RESET_ALL}\n")