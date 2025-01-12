
from colorama import Fore, Back, Style
import colorama

colorama.init()

# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA (purple), CYAN (Turquoise), WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.


class Colors:

    def __init__(self):
        # Server status colors
        self.SERVER_STATUS = Fore.MAGENTA

        self.CLIENT_STATUS = Fore.CYAN

        # Message types
        self.INFO = Fore.MAGENTA
        self.SUCCESS = Fore.GREEN
        self.ERROR = Fore.RED

        # Transfer status
        self.TCP_TRANSFER = Fore.BLUE
        self.UDP_TRANSFER = Fore.CYAN

        # Statistics
        self.STATS = Fore.YELLOW

        # Values/Numbers
        self.VALUES = Fore.WHITE

        # Highlights
        self.HIGHLIGHT = Back.BLUE + Fore.WHITE

        # Reset
        self.RESET = Style.RESET_ALL

    @staticmethod
    def format_error(message):
        return f"{Fore.RED}{message}{Style.RESET_ALL}"

    @staticmethod
    def format_success(message):
        return f"{Fore.GREEN}{message}{Style.RESET_ALL}"

    @staticmethod
    def format_tcp_transfer(transfer_num, duration, speed):
        return (f"{Fore.BLUE}TCP transfer #{Fore.YELLOW}{transfer_num}{Fore.BLUE} finished, "
                f"total time: {Fore.YELLOW}{duration:.2f}{Fore.BLUE} seconds, "
                f"total speed: {Fore.YELLOW}{speed:.1f}{Fore.BLUE} bits/second{Style.RESET_ALL}")

    @staticmethod
    def format_udp_transfer(transfer_num, duration, speed, success_rate):
        return (f"{Fore.MAGENTA}UDP transfer #{Fore.YELLOW}{transfer_num}{Fore.MAGENTA} finished, "
                f"total time: {Fore.YELLOW}{duration:.2f}{Fore.MAGENTA} seconds, "
                f"total speed: {Fore.YELLOW}{speed:.1f}{Fore.MAGENTA} bits/second, "
                f"percentage of packets received successfully: {Fore.YELLOW}{success_rate:.0f}%{Style.RESET_ALL}")