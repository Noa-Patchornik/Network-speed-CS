import socket
import struct
import time

from NetworkCS.Colors import Colors
from NetworkCS.Configuration import Configuration


class RequestTransfer:
    def __init__(self):
        # using configuration file to avoid hard coding definitions
        self.config = Configuration().get_config()
        # add support in colorful console as requested
        self.colors = Colors()

    def tcp_transfer(self, server_ip, port, file_size, transfer_num):
        """
        tcp transfer request to server
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((server_ip, port))
                s.send(f"{file_size}\n".encode())

                # calculate time for later on speed calculation
                start_time = time.time()
                # for constructing the recieved data later on
                received_data = b''
                bytes_received = 0

                # recive until no more, but according to the buffer size that in config file

                while bytes_received < file_size:
                    # in case of remaining less than buffer size bytes
                    chunk = s.recv(min(self.config.buffer_size, file_size - bytes_received))
                    if not chunk:
                        break
                    received_data += chunk
                    bytes_received += len(chunk)

                # in case of valid packet, print different details to console according to the requirements
                if self.verify_packet(file_size, received_data):
                    duration = max(time.time() - start_time, 0.001)
                    # for calculation in bits/seconds
                    speed = (file_size * 8) / duration
                    print(self.colors.format_tcp_transfer(transfer_num, duration, speed))
                else:
                    raise Exception("Failed due to incomplete data transfer")

        except Exception as e:
            print(self.colors.format_error(f"Error in TCP transfer #{transfer_num}: {e}"))

    def udp_transfer(self, server_ip, udp_port, file_size, transfer_num):
        """
        udp transfer request to server
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                # create a request msg from client to server
                request = self.construct_request_msg(file_size)
                # send it to server
                s.sendto(request, (server_ip, udp_port))
                print(self.colors.CLIENT_STATUS + f"Sent UDP request for {file_size} bytes\n" + self.colors.RESET)

                start_time = time.time()
                received_segments = set()
                total_segments = None
                last_receive_time = time.time()

                s.settimeout(0.1)

                # handling reciving data form server
                while True:
                    try:
                        data, _ = s.recvfrom(self.config.buffer_size)
                        last_receive_time = time.time()

                        # validate the msg
                        seg_num, total_segs = self.validate_payload_msg(data)

                        if seg_num is None:
                            continue

                        if total_segments is None:
                            total_segments = total_segs
                            print(self.colors.INFO + f"Expecting {total_segments} segments\n" + self.colors.RESET)

                        received_segments.add(seg_num)
                        # printing every 100 segemnts to console for indicating the process
                        if len(received_segments) % 100 == 0:
                            print(self.colors.CLIENT_STATUS +
                                  f"Received {len(received_segments)} unique segments\n" +
                                  self.colors.RESET)


                    # in case of an error
                    except socket.timeout:
                        # just to make sure not to exceed the 1.0 sec
                        if time.time() - last_receive_time >= 1.0:
                            break
                        continue
                    except Exception as e:
                        print(self.colors.format_error(f"Error receiving packet: {e}\n"))
                        continue

                duration = max(time.time() - start_time, 0.001)
                speed = (file_size * 8) / duration
                success_rate = (len(received_segments) / total_segments * 100) if total_segments else 0

                print(self.colors.format_udp_transfer(transfer_num, duration, speed, success_rate))

        except Exception as e:
            print(self.colors.format_error(f"Error in UDP transfer #{transfer_num}: {e}\n"))

    def construct_request_msg(self, file_size):
        """
        constructing request msgs
        """
        return struct.pack('!IBQ',
                           self.config.cookie,
                           self.config.request_message_type,
                           file_size
                           )

    def validate_payload_msg(self, data):
        """
        validate the payload msg according to the requirements written in the mission
        """
        header_size = struct.calcsize('!IBQQ')
        if len(data) >= header_size:
            try:
                header = data[:header_size]
                cookie, msg_type, total_segs, seg_num = struct.unpack('!IBQQ', header)
                if cookie == self.config.cookie and msg_type == self.config.payload_message_type:
                    return seg_num, total_segs
            except struct.error:
                pass
        return None, None

    def verify_packet(self, file_size, data):
        """
        verify packet details, the same length as expected and conent
        """
        # checks length
        received_size = len(data)
        if received_size != file_size:
            print(self.colors.format_error("Error: Received {received_size} bytes, expected {file_size}\n"))
            return False
        # checks content
        if data != self.config.dummy_bit * file_size:
            print(self.colors.format_error("Error: Received data doesn't match expected content\n"))
            return False
        # in case of success reciving
        return True
