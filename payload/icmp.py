from ping3 import ping, verbose_ping

def ping_host(host):
    response_time = ping(host, timeout=4)
    if response_time:
        print(f"{host} is reachable (Response Time: {response_time} ms).")
    else:
        print(f"{host} is unreachable.")

if __name__ == "__main__":
    host_to_ping = input("Enter the host to ping: ")
    ping_host(host_to_ping)

"""
import socket
import os
import struct
import time

def checksum(data):
    csum = 0
    countTo = (len(data) // 2) * 2

    for count in range(0, countTo, 2):
        thisVal = data[count + 1] * 256 + data[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff

    if countTo < len(data):
        csum = csum + data[-1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    result = ~csum
    result = result & 0xffff
    result = result >> 8 | (result << 8 & 0xff00)
    return result

def send_ping_request(dest_addr, timeout=1):
    icmp = socket.getprotobyname("icmp")
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)

    my_id = os.getpid() & 0xFFFF

    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    header = struct.pack("bbHHh", 8, 0, 0, my_id, 1)
    data = struct.pack("d", time.time())

    # Calculate the checksum on the data and the dummy header.
    my_checksum = checksum(header + data)

    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack("bbHHh", 8, 0, socket.htons(my_checksum), my_id, 1)
    packet = header + data

    try:
        sock.sendto(packet, (dest_addr, 1))
        start_time = time.time()
        sock.settimeout(timeout)
        sock.recvfrom(1024)
        return time.time() - start_time
    except socket.timeout:
        return None
    finally:
        sock.close()

if __name__ == "__main__":
    host_to_ping = input("Enter the host to ping: ")
    response_time = send_ping_request(host_to_ping)
    if response_time is not None:
        print(f"Ping to {host_to_ping} successful (Response Time: {response_time * 1000:.2f} ms).")
    else:
        print(f"Ping to {host_to_ping} timed out.")

"""