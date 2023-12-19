from scapy.all import *
from netfilterqueue import NetfilterQueue
import netifaces
import zstandard as zstd
from dotenv import load_dotenv
import subprocess
import json 
import multiprocessing
import time
# import zlib
# import os
load_dotenv()

# Define a flag to indicate whether a packet is compressed
COMPRESSION_FLAG = b'\x01'
DECOMPRESSION_FLAG = b'\x00'

if len(sys.argv) != 2:
    print("python main.py host_id ")
    sys.exit(1)

host_id = sys.argv[1]
time_interval = 0.5

# Important stuffs about zstandard package
# write_content_size parameter improves performance
# one-shot vs streaming modes
# dictionaries
# compression_params?
# Multithreading

avg_compression_ratio = 1.5
sum_samples = 1 
avg_compression_time = 0.01

def compress_time():
    global avg_compression_time
    return avg_compression_time

def decompress_time():
    global avg_compression_time
    return avg_compression_time

def transit_time(file_size, time_interval, host_id, transit_time_cache):
    args = ["python", "TRANSIT_TIME/main.py", str(file_size), str(time_interval), str(host_id)]
    result =  subprocess.run(args, text=True, capture_output=True).stdout.split('\n').strip()
    print(result[0])
    transit_time_cache.value = result[0]
    


def update_transit_time(file_size, time_interval, host_id, transit_time_cache):
    while True:
        transit_time(file_size, time_interval, host_id, transit_time_cache)
        print(transit_time_cache.value)
        time.sleep(time_interval*20)

def check_condition(file_size, transit_time_cache):
    lhs = compress_time() +  file_size / (transit_time_cache.value *  avg_compression_ratio) + decompress_time() 
    rhs = file_size / transit_time_cache.value

    return lhs < rhs

def process_packet(packet, transit_time_cache):
    payload = packet.get_payload()
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(Raw):
        ip_header = scapy_packet[IP]
        source_ip = ip_header.src
        payload = bytes(scapy_packet[Raw])

        if scapy_packet.haslayer(TCP)==False:
            scapy_packet[TCP] = None
        else:
            tcp_header = scapy_packet[TCP]
        #if source_ip in host_ips :
        if True :
            print("Outgoing Traffic:")
            global sum_samples
            global avg_compression_time
            global avg_compression_ratio
            #if(sum_samples <=2 or check_condition(len(payload), transit_time_cache)):
            if True:
                compressiontime = time.time()
                compressed_payload = cctx.compress(payload)
                compressiontime = time.time() - compressiontime
                sum_samples+=1;
                avg_compression_time = (sum_samples -1)*avg_compression_time + compressiontime / sum_samples
                avg_compression_ratio = ((sum_samples - 1)*avg_compression_ratio + len(payload)/len(compressed_payload) )/ sum_samples
                # Consider UDP
                compressed_packet = IP(src=ip_header.src, dst=ip_header.dst) / TCP(sport=tcp_header.sport,dport=tcp_header.dport)
                compressed_packet = compressed_packet / compressed_payload
            else:
                compressed_payload = payload
            #compressed_payload = zlib.compress(payload,level=9)
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

if __name__ == '__main__':
    with multiprocessing.Manager() as manager:

        transit_time_cache = manager.Value('f',0.001)

        pool = multiprocessing.Pool(processes = 1)


        interfaces = netifaces.interfaces()
        host_ips = []
        for interface in interfaces:
            addrs = netifaces.ifaddresses(interface)
            if 2 in addrs.keys():
                host_ips.append(addrs[netifaces.AF_INET][0]['addr'])

        QUEUE_NUM = int(os.environ.get("QUEUE_NUM"))

        samples = []

        files = [f for f in os.listdir('./github') if os.path.isfile(os.path.join('./github', f))]
        for file_name in files:
                 file_path = os.path.join('./github', file_name)
                 with open(file_path, 'r') as file:
                     data = file.read()
                     samples.append(str(data))

        print(len(samples))
        samples = [bytes(sample, 'utf-8') for sample in samples]
        dict_data = zstd.train_dictionary(275,samples)
        with open("dict_data", "w") as f:
            f.write(str(dict_data.as_bytes()))

        pool.apply_async(update_transit_time, (len(dict_data), time_interval, host_id, transit_time_cache))

        cctx = zstd.ZstdCompressor(level=3,write_content_size=False)
        dctx = zstd.ZstdDecompressor()
        nfqueue = NetfilterQueue()
        nfqueue.bind(QUEUE_NUM, lambda packet: process_packet(packet, transit_time_cache))
        nfqueue.run()

        pool.close()
        pool.join()
