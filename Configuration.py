class Configuration:
    def __init__(self):
        self.config = {
            'cookie': 0xabcddcba, #cookie as requested
            #messages type so differ them
            'offer_message_type': 0x2,
            'request_message_type': 0x3,
            'payload_message_type': 0x4,
            #random ports one for each protocol
            'udp_port': 13117,
            'tcp_port': 23456,
            #'tcp_port': 20000,
            #messages length
            'payload_len' : 21,
            'offer_len' : 9,
            'request_len': 13,
            'dummy_bit' : b'1', #creat data with the requested size
            'buffer_size' : 1024, #buffer size to send data

        }

    def get_config(self):
        return type('Config', (), self.config)


