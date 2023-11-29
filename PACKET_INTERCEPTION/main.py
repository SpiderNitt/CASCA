from scapy.all import *
from netfilterqueue import NetfilterQueue
import socket
import sys

def compress_packet(packet):
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(Raw):
        print(scapy_packet[TCP].payload)
        # coflow schedule and compression
    packet.accept()

def decompress_packet(packet):
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(Raw):
        print(scapy_packet[TCP].payload)
        # coflow schedule and compression
    packet.accept()

COMPRESS_QUEUE_NUM = 1
DECOMPRESS_QUEUE_NUM = 2

print('Listening on NFQUEUE queue-num {} for compression'.format(COMPRESS_QUEUE_NUM))
print('Listening on NFQUEUE queue-num {} for decompression'.format(DECOMPRESS_QUEUE_NUM))

nfqueue1 = NetfilterQueue()
nfqueue2 = NetfilterQueue()
nfqueue1.bind(COMPRESS_QUEUE_NUM, compress_packet)
nfqueue2.bind(DECOMPRESS_QUEUE_NUM, decompress_packet)
s1 = socket.fromfd(nfqueue1.get_fd(), socket.AF_UNIX, socket.SOCK_STREAM)
s2 = socket.fromfd(nfqueue2.get_fd(), socket.AF_UNIX, socket.SOCK_STREAM)
try:
    nfqueue1.run_socket(s1)
    nfqueue2.run_socket(s2)
except KeyboardInterrupt:
    sys.stdout.write('Exiting \n')

s1.close()
s2.close()
nfqueue1.unbind()
nfqueue2.unbind()