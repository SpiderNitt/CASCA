from scapy.all import *
from netfilterqueue import NetfilterQueue
import netifaces
import zstandard as zstd
from dotenv import load_dotenv
import json 
import lz4.frame
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
        ip_header = scapy_packet[IP]
        if scapy_packet.haslayer(TCP)==False:
            scapy_packet[TCP] = None
        else:
            tcp_header = scapy_packet[TCP]

        # if scapy_packet.haslayer(UDP)==False:
        #     scapy_packet[UDP] = None
        # elif scapy_packet.haslayer(Raw)==False:
        #     scapy_packet[Raw] = None
        
        source_ip = ip_header.src
        payload = bytes(scapy_packet[Raw])
        # Outgoing packets(Compression)
        if source_ip in host_ips:
            print("Outgoing Traffic:")
            # print(scapy_packet[TCP].summary())
            # print(type(payload))
            # with open('README.md','rb') as f:
            #     payload = f.read()
            # compressed_payload = cctx.compress(payload)
            
            compressed_payload = cctx.compress(payload)
            # Consider UDP
            compressed_packet = IP(src=ip_header.src, dst=ip_header.dst) / TCP(sport=tcp_header.sport,dport=tcp_header.dport)
            compressed_packet = compressed_packet / compressed_payload
            print("Original Payload size:", len(payload))
            print("Compressed Payload size:", len(compressed_payload))
            # compressed_packet.accept()
            packet.set_payload(bytes(compressed_packet))
        else: # Incoming packets(Decompression)
            print(scapy_packet[IP].src)
            if scapy_packet[IP].src=="192.168.43.167":
                print("Incoming Traffic:")
                # print(scapy_packet[TCP].summary())
                #print(payload)
                # start_time = time.time()
                decompressed_payload = dctx.decompress(payload, max_output_size=1048576)
                # end_time = time.time()
                # print(start_time-end_time)
                decompressed_packet = IP(src=ip_header.src, dst=ip_header.dst) / TCP(sport=tcp_header.sport,dport=tcp_header.dport)

                decompressed_packet = decompressed_packet / decompressed_payload

                #decompressed_payload = zlib.decompress(payload)
                print("Original Payload size:", len(payload))
                # print("Payloads length: ",len(payloads))
                print("Decompressed Payload size:", len(decompressed_payload))
                # packet.set_payload(decompressed_payload)
                # decompressed_packet.accept()
                packet.set_payload(bytes(decompressed_packet))
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
for i in range(1,16):
    with open(f'./captured_packets/captured_payloads{i}.json','rb') as f:
        samples+=[f.read()]
# files = [f for f in os.listdir('./github') if os.path.isfile(os.path.join('./github', f))]
# for file_name in files:
#         file_path = os.path.join('./github', file_name)
#         with open(file_path, 'r') as file:
#             data = file.read()
#             samples.append(str(data))
print(len(samples))
# samples = [sample for sample in samples]
# print(samples)
dict_data = zstd.train_dictionary(275,samples)
with open("dict_data", "w") as f:
    f.write(str(dict_data.as_bytes()))

cctx = zstd.ZstdCompressor(level=3,write_content_size=False)
dctx = zstd.ZstdDecompressor()
nfqueue = NetfilterQueue()
nfqueue.bind(QUEUE_NUM, process_packet)
nfqueue.run()
