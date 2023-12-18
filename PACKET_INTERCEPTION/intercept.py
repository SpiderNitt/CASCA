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
    global payloads
    global i
    if scapy_packet.haslayer(Raw):
            print("Incoming Traffic:")
            # print(scapy_packet[TCP].summary())
            #print(payload)
            #decompressed_payload = dctx.decompress(payload)
            #decompressed_payload = zlib.decompress(payload)
            if len(payloads)==1000:
                i+=1
                payloads = []
            payloads.append(str(bytes(payload)))
            with open(f"./captured_packets/captured_payloads{i}.json",'w') as f:
                json.dump({'payloads':payloads},f)
            print("Original Payload size:", len(payload))
            print("Payloads length: ",len(payloads))
            # print("Decompressed Payload size:", len(decompressed_payload))
            # packet.set_payload(decompressed_payload)
        # print(scapy_packet.show())
        # coflow schedule and compression
    packet.accept()

i = 11
global payloads
with open(f"./captured_packets/captured_payloads{i}.json") as f:
    payloads = json.load(f)['payloads']
print(len(payloads))
interfaces = netifaces.interfaces()
host_ips = []
for interface in interfaces:
    addrs = netifaces.ifaddresses(interface)
    if 2 in addrs.keys():
        host_ips.append(addrs[netifaces.AF_INET][0]['addr'])

QUEUE_NUM = int(os.environ.get("QUEUE_NUM"))


cctx = zstd.ZstdCompressor()
dctx = zstd.ZstdDecompressor()
nfqueue = NetfilterQueue()
nfqueue.bind(QUEUE_NUM, process_packet)
nfqueue.run()
