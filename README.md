

# Network Speed Test - Client-Server Application

# Introduction
This project implements a client-server application designed for network speed testing. 
It allows you to compare UDP and TCP download speeds, providing insights into how they 
share the same network. The application supports multi-threading for both the client and 
server, enabling simultaneous transfers using both protocols.

# Features:
# Client:
Multithreaded with three distinct states:
- Startup: Collect user parameters.
- Looking for a server: Wait for an offer from a server.
- Speed test: Launch multiple threads for TCP and UDP connections to transfer data.

# Server:
Multithreaded with threads for:
- Broadcasting offer messages.
- UDP supports three packet types: offer, request, and payload.
- TCP supports standard file transfers.

# File Structure
# Server Package:
Server: The main server application that listens for incoming requests.
UDPHandler: Handles UDP requests and responses.
TCPHandler: Manages TCP connections.
PayloadSender: Responsible for sending payloads in response to UDP requests.
OfferBroadcaster: Periodically broadcasts UDP offer messages to clients.

# Client Package:
Client: The main client application that interacts with the server and performs speed tests.
ClientHandler: Manages the client's interactions with the server.
Listener: Listens for incoming offer messages and handles connections.
RequestTransfer: Manages the actual transfer of data over both UDP and TCP.

# Configuration
The configuration file allows easy modification of the following parameters:

- cookie: The cookie (4 bytes) used for packet validation. 
Any message that doesn't start with this cookie will be rejected.
- offer_message_type: Specifies the message type for offer packets sent from the server 
to the client.
- request_message_type: Specifies the message type for request packets sent from the 
client to the server.
- payload_message_type: Specifies the message type for payload packets sent from the 
server to the client.
- udp_port: The port number used for the UDP protocol.
- tcp_port: The port number used for the TCP protocol.
- payload_len: The length of the payload message (in bytes) for each UDP packet.
- offer_len: The length of the offer message sent by the server.
- dummy_bit: A dummy bit used in certain packet types.
- request_len: The length of the request message sent by the client.
- buffer_size: The buffer size used for data transfer operations.
- server_ip: The IP address of the server. 


