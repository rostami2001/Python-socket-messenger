import socket
import time
import random

RTT = 0.1
PACKET_LOSS_RATE = 0.1
CONGESTION_WINDOW_SIZE = 4

packet_in_flight = 0

# Server configuration
SERVER_ADDRESS = ('localhost', 12345)

# Added for Reno algorithm
RETRANSMISSION_TIMEOUT = 0.5  # Timeout for retransmitting packets

def send_packet(packet_number, sock):
    global packet_in_flight
    print(f"Sending packet {packet_number}")

    if random.random() < PACKET_LOSS_RATE:
        print("Packet Lost!")
    else:
        try:
            sock.sendall(f"Packet {packet_number}".encode())
            time.sleep(RTT)
            packet_in_flight += 1
        except socket.error as e:
            print(f"Error sending packet {packet_number}: {e}")

def wait_for_ack(sock):
    # Simulate waiting for ACK
    try:
        data = sock.recv(1024)
        if data:
            print(f"Received ACK: {data.decode()}")
            return True
    except socket.timeout:
        return False

def timeout_or_packet_loss():
    global packet_in_flight
    print("Timeout or packet loss occurred")
    packet_in_flight = 0  # Reset the number of packets in flight

def retransmit_packets(sock):
    global packet_in_flight
    print("Retransmitting packets...")
    for i in range(packet_in_flight):
        send_packet(i, sock)

def initialize():
    # Initialize socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(RETRANSMISSION_TIMEOUT)  # Set timeout for the socket
    sock.connect(SERVER_ADDRESS)

    return sock

# Example usage
sock = initialize()

for i in range(10):
    send_packet(i, sock)

    # Simulate waiting for ACKs
    ack_received = wait_for_ack(sock)

    # Check for timeout or packet loss
    if packet_in_flight > CONGESTION_WINDOW_SIZE or not ack_received:
        timeout_or_packet_loss()
        retransmit_packets(sock)  # Retransmit packets on timeout

# Close the socket when done
sock.close()
