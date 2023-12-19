from scapy.all import *
from netfilterqueue import NetfilterQueue
import netifaces
import zstandard as zstd
from dotenv import load_dotenv
import json 
load_dotenv()

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
        if source_ip in host_ips: # Outgoing packets(Compression)
            print("Outgoing Traffic:")
            start_time = time.time()
            compressed_payload = cctx.compress(payload)
            end_time = time.time()
            print("Compression time: ", end_time-start_time)
            # Consider UDP
            compressed_packet = IP(src=ip_header.src, dst=ip_header.dst) / TCP(sport=tcp_header.sport,dport=tcp_header.dport)
            compressed_packet = compressed_packet / compressed_payload
            print("Original Payload size:", len(payload))
            print("Compressed Payload size:", len(compressed_payload))
            packet.set_payload(bytes(compressed_packet))
        else: # Incoming packets(Decompression)
            print("Incoming Traffic:")
            start_time = time.time()
            decompressed_payload = dctx.decompress(payload, max_output_size=1048576)
            end_time = time.time()
            print("Decompression time: ", end_time-start_time)
            decompressed_packet = IP(src=ip_header.src, dst=ip_header.dst) / TCP(sport=tcp_header.sport,dport=tcp_header.dport)
            decompressed_packet = decompressed_packet / decompressed_payload
            print("Original Payload size:", len(payload))
            print("Decompressed Payload size:", len(decompressed_payload))
            packet.set_payload(bytes(decompressed_packet))
    packet.accept()

interfaces = netifaces.interfaces()
host_ips = []
for interface in interfaces:
    addrs = netifaces.ifaddresses(interface)
    if 2 in addrs.keys():
        host_ips.append(addrs[netifaces.AF_INET][0]['addr'])

QUEUE_NUM = int(os.environ.get("QUEUE_NUM"))

cctx = zstd.ZstdCompressor(level=3,write_content_size=False)
dctx = zstd.ZstdDecompressor()
nfqueue = NetfilterQueue()
nfqueue.bind(QUEUE_NUM, process_packet)
nfqueue.run()
