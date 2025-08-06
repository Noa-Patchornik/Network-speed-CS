

# Network Speed Test - Client-Server Application

# Introduction
A Python-based simulation framework designed to evaluate and compare TCP and UDP performance under varying file sizes and connection loads.
The project consists of a client-server model, where the client requests a file of configurable size, and the server transmits it via multiple parallel TCP/UDP connections.

The goal is to simulate a realistic network load and analyze throughput, speed, and reliability for each transport protocol.

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
- Server: The main server application that listens for incoming requests.
- UDPHandler: Handles UDP requests and responses.
- TCPHandler: Manages TCP connections.
- PayloadSender: Responsible for sending payloads in response to UDP requests.
- OfferBroadcaster: Periodically broadcasts UDP offer messages to clients.

# Client Package:
- Client: The main client application that interacts with the server and performs speed tests.
- ClientHandler: Manages the client's interactions with the server.
- Listener: Listens for incoming offer messages and handles connections.
- RequestTransfer: Manages the actual transfer of data over both UDP and TCP.

# How It Works – Protocol Flow
# 1) Broadcast Discovery (UDP)
  - The server broadcasts an "offer" every second on a predefined port.
  - The client capture these offers.
  - When a valid offer is received, the client initiates a connection.

# 2) Client Configuration Input
  - The user is prompted to enter:
    - File size (in units like KB, MB, Gb, etc.)
    - Number of TCP connections to open
    - Number of UDP connections to open

# 3) File Transfer Begins
  - For each TCP connection:
    - A reliable stream is established.
    - The file is sent in chunks until fully received.
    - Total speed and duration are measured.

  - For each UDP connection:
    - A single request packet is sent.
    - The server replies with multiple payload packets.
    - The client calculates the total segments received, speed, and success rate.

# 4) Performance Output
  - The client prints a breakdown for each connection:
  - Total time
  - Total speed (bits/sec)
  - Percentage of successful packet receipt (UDP only)

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


