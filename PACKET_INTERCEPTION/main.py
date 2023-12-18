from scapy.all import *
from netfilterqueue import NetfilterQueue
import netifaces
import zstandard as zstd
from dotenv import load_dotenv
import json 
# import zlib
# import os
load_dotenv()

# Important stuffs about zstandard package
# write_content_size parameter improves performance
# one-shot vs streaming modes
# dictionaries
# compression_params?
# Multithreading

def process_packet(packet):
    payload = packet.get_payload()
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(Raw):
        source_ip = scapy_packet[IP].src
        # Outgoing packets(Compression)
        if source_ip in host_ips:
            print("Outgoing Traffic:")
            # print(scapy_packet[TCP].summary())
            #print(payload)
            compressed_payload = cctx.compress(payload)
            #compressed_payload = zlib.compress(payload,level=9)
            print("Original Payload size:", len(payload))
            print("Compressed Payload size:", len(compressed_payload))
            packet.set_payload(compressed_payload)
        else: # Incoming packets(Decompression)
            print("Incoming Traffic:")
            # print(scapy_packet[TCP].summary())
            #print(payload)
            #decompressed_payload = dctx.decompress(payload)
            #decompressed_payload = zlib.decompress(payload)
            print("Original Payload size:", len(payload))
            print("Payloads length: ",len(payloads))
            # print("Decompressed Payload size:", len(decompressed_payload))
            # packet.set_payload(decompressed_payload)
        # print(scapy_packet.show())
        # coflow schedule and compression
    packet.accept()

interfaces = netifaces.interfaces()
host_ips = []
for interface in interfaces:
    addrs = netifaces.ifaddresses(interface)
    if 2 in addrs.keys():
        host_ips.append(addrs[netifaces.AF_INET][0]['addr'])

QUEUE_NUM = int(os.environ.get("QUEUE_NUM"))

samples = []
for i in range(1,6):
    with open(f'./captured_packets/captured_payloads{i}.json') as f:
        samples+=json.load(f)['payloads']
print(len(samples))
samples = [bytes(sample, 'utf-8') for sample in samples]
dict_data = zstd.train_dictionary(len(samples),samples)
with open("dict_data", "w") as f:
    f.write(str(dict_data.as_bytes()))

cctx = zstd.ZstdCompressor(dict_data=dict_data)
dctx = zstd.ZstdDecompressor(dict_data=dict_data)
nfqueue = NetfilterQueue()
nfqueue.bind(QUEUE_NUM, process_packet)
nfqueue.run()
