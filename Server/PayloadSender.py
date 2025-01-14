import struct
import time
import traceback

from Colors import Colors
from Configuration import Configuration

""" Class that sends the requested data that the client asked"""
class PayloadSender:
    def __init__(self):
        # add support in colorful console as requested
        self.colors = Colors()
        # using configuration file to avoid hard coding definitions
        self.config = Configuration().get_config()

    def send_file_udp(self, udp_socket, client_addr, file_size):
        """
        Sends file data via UDP in segments
        """
        buffer_size = self.config.buffer_size
        total_segments = (file_size + buffer_size - 1) // buffer_size

        # Send each segment as a payload message
        for segment_num in range(total_segments):
            try:
                # Construct and send packet
                packet = self.construct_payload_msg(total_segments, segment_num)
                udp_socket.sendto(packet, client_addr)
                # Print progress every 100 segments
                if segment_num % 100 == 0:
                    print(self.colors.SERVER_STATUS +
                          f"Sent segment {segment_num + 1}/{total_segments}\n" +
                          self.colors.RESET)

                # Small delay to prevent network flooding
                time.sleep(0.001)

            except Exception as e:
                traceback.print_exc()
                print(self.colors.format_error(f"Error sending segment {segment_num + 1}: {e}"))



    def construct_payload_msg(self,total_segments,segment_num):
        """
        constructing the payload msg according to the requirements
        """
        header = struct.pack('!IBQQ',
                             self.config.cookie,
                             self.config.payload_message_type,
                             total_segments,
                             segment_num + 1)
        payload = self.config.dummy_bit
        packet = header + payload
        return packet
