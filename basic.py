import socket

# UDP port to listen on
UDP_PORT = 4210

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Bind the socket to the port
sock.bind(('', UDP_PORT))

print(f"Listening for discovery messages on UDP port {UDP_PORT}")

while True:
    # Receive message from the UDP socket
    data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
    print(f"Received message: {data.decode()} from {addr}")
