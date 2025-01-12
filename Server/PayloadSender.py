import struct
import time

from Colors import Colors
from Configuration import Configuration


class PayloadSender:
    def __init__(self):
        # add support in colorful console as requested
        self.colors = Colors()
        # using configuration file to avoid hard coding definitions
        self.config = Configuration().get_config()

    def send_file_udp(self, udp_socket, client_addr, file_size):
        #sending the file as payload msg in udp connection
        buffer_size = self.config.buffer_size

        #making sure that there is enough segments to send all the data requested
        total_segments = (file_size + buffer_size - 1) // buffer_size

        # Pre-generate the dummy data
        segment_data = self.config.dummy_bit * buffer_size
        last_segment_size = file_size % buffer_size
        last_segment_data = self.config.dummy_bit * (last_segment_size if last_segment_size != 0 else buffer_size)

        for segment_num in range(total_segments):
            # Use pre-generated data
            current_data = last_segment_data if segment_num == total_segments - 1 else segment_data
            packet = self.construct_payload_msg(total_segments, segment_num) + current_data

            try:
                udp_socket.sendto(packet, client_addr)
                if segment_num % 100 == 0:
                    print(self.colors.SERVER_STATUS +
                          f"Sent segment {segment_num + 1}/{total_segments}" +
                          self.colors.RESET)
                time.sleep(0.001)
            except Exception as e:
                print(self.colors.format_error(f"Error sending segment {segment_num + 1}: {e}"))


    def construct_payload_msg(self,total_segments,segment_num):
        """
        constructing the payload msg according to the requirements
        """
        header = struct.pack('!IBQQ',
                             self.config.cookie,
                             self.config.payload_message_type,
                             total_segments,
                             segment_num + 1
                             )
        payload = self.config.dummy_bit
        packet = header + payload
        return packet
