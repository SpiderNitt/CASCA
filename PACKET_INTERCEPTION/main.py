from scapy.all import *
from netfilterqueue import NetfilterQueue
import netifaces
import zstandard as zstd
from dotenv import load_dotenv
import subprocess
import json 
# import zlib
# import os
load_dotenv()

if len(sys.argv) != 2:
    print("python main.py host_id ")
    sys.exit(1)

host_id = sys.argv[1]
time_interval = 1.5

# Important stuffs about zstandard package
# write_content_size parameter improves performance
# one-shot vs streaming modes
# dictionaries
# compression_params?
# Multithreading

avg_compression_ratio = 0
sum_samples = 0 
avg_compression_time = 0

def compress_time():
    print("compress")
    return avg_compression_time

def decompress_time():
    print("decompress")
    return avg_comrpession_time

def transit_time(file_size, time_interval, host_id):
    print("time")
    
    args = ["python", "TRANSIT_TIME/__main__.py", str(file_size), str(time_interval), str(host_id)]
    print(' '.join(args))

    return float(subprocess.run(args, text=True, capture_output=True).stdout.split())
    

def check_condition(file_size):
    print("hello")
    lhs = compress_time() + transit_time(file_size / avg_compression_time, time_interval, host_id) + decompress_time() 
    print(lhs)
    rhs = transit_time(file_size , time_interval, host_id)
    print(rhs)
    print(lhs<rhs)
    return lhs < rhs

def process_packet(packet):
    payload = packet.get_payload()
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(Raw):
        source_ip = scapy_packet[IP].src
        # Outgoing packets(Compression)
        #if source_ip in host_ips :
        if True :
            print("Outgoing Traffic:")
            # print(scapy_packet[TCP].summary())
            #print(payload)
            global sum_samples
            global avg_compression_time
            global avg_compression_ratio
            if(sum_samples <=2 or check_condition(len(payload))):
                compressiontime = time.time()
                compressed_payload = cctx.compress(payload)
                compressiontime = time.time() - compressiontime
                sum_samples+=1;
                avg_compression_time = (sum_samples -1)*avg_compression_time + compressiontime / sum_samples
                avg_compression_ratio = ((sum_samples - 1)*avg_compression_ratio + len(payload)/len(compressed_payload) )/ sum_samples
            else:
                compressed_payload = payload
            #compressed_payload = zlib.compress(payload,level=9)
            print("Original Payload size:", len(payload))
            print("Compressed Payload size:", len(compressed_payload))
            packet.set_payload(compressed_payload)
        else: # Incoming packets(Decompression)
            print("Incoming Traffic:")
            # print(scapy_packet[TCP].summary())
            #print(payload)
            decompressed_payload = dctx.decompress(payload)
            #decompressed_payload = zlib.decompress(payload)
            print("Original Payload size:", len(payload))
            # print("Payloads length: ",len(payloads))
            print("Decompressed Payload size:", len(decompressed_payload))
            packet.set_payload(decompressed_payload)
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
    with open(f'./captured_packets/captured_payloads{i}.json') as f:
        samples+=(json.load(f)['payloads'])

# files = [f for f in os.listdir('./github') if os.path.isfile(os.path.join('./github', f))]
# for file_name in files:
#         file_path = os.path.join('./github', file_name)
#         with open(file_path, 'r') as file:
#             data = file.read()
#             samples.append(str(data))

print(len(samples))
samples = [bytes(sample, 'utf-8') for sample in samples]
dict_data = zstd.train_dictionary(275,samples)
with open("dict_data", "w") as f:
    f.write(str(dict_data.as_bytes()))


cctx = zstd.ZstdCompressor(dict_data=dict_data)
dctx = zstd.ZstdDecompressor(dict_data=dict_data)
nfqueue = NetfilterQueue()
nfqueue.bind(QUEUE_NUM, process_packet)
nfqueue.run()
