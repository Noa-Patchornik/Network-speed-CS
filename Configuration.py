class Configuration:
    def __init__(self):
        self.config = {
            'cookie': 0xabcddcba,
            'offer_message_type': 0x2,
            'request_message_type': 0x3,
            'payload_message_type': 0x4,
            'udp_port': 13117,
            'tcp_port': 23456,
            'payload_len' : 21,
            'offer_len' : 9,
            'dummy_bit' : b'1',
            'request_len' : 13,
            'buffer_size' : 1024,
            'server_ip' : '0.0.0.0'

        }

    def get_config(self):
        return type('Config', (), self.config)


