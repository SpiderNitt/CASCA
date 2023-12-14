from scapy.all import *
from netfilterqueue import NetfilterQueue
import socket
import sys

def process_packet(packet):
    compression_rate=0.6 #hardcoded compression rate
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(Raw):
        print(scapy_packet[TCP].payload)
        # coflow schedule and compression
    scapy_packet = IP(packet.get_payload())/Raw(load=compression_rate)
    packet.set_payload(scapy_packet)
    packet.accept()

QUEUE_NUM = 1

print('Listening on NFQUEUE queue-num {}'.format(QUEUE_NUM))

nfqueue = NetfilterQueue()
nfqueue.bind(QUEUE_NUM, process_packet)
s = socket.fromfd(nfqueue.get_fd(), socket.AF_UNIX, socket.SOCK_STREAM)
try:
    nfqueue.run_socket(s)
except KeyboardInterrupt:
    sys.stdout.write('Exiting \n')

s.close()
nfqueue.unbind()