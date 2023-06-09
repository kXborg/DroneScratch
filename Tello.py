import threading
import socket
import sys
import time
import platform  

host = ''
port = 9000
locaddr = (host,port) 


# Create a UDP socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Setup UDP server.
sock.bind(locaddr)

# Tello address to send command and receive response.
tello_address = ('192.168.10.1', 8889)


def recv():
    count = 0
    while True:
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break


# create receiving thread to run concurrently.
recvThread = threading.Thread(target=recv)
recvThread.start()

while True: 
    try:
        msg = input("")

        if not msg:
            break  

        if 'end' in msg:
            print ('...')
            sock.close()  
            break

        # Send data.
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, tello_address)

    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()  
        break




