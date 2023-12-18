import psutil
import time 
import csv
import zstandard
import os
import sys
import stressinjector as injector
import resource
import math

output_file = 'system_stats.csv'
path = sys.argv[1]

# Run this code on different hardware specifications

with open(output_file,'a',newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Timestamp", "No of CPUs", "CPU Utilization (%)", "CPU Frequency (Mhz)", "Memory (MB)", "Memory Utilization (%)", "Compression Speed (MB/s)", "Compression Ratio", "Packet size difference rate"])

    compressor = zstandard.ZstdCompressor(level=3)

    cpus = psutil.cpu_count()# Considers logical cores also    
    memory = psutil.virtual_memory().total/(1024*1024)# Get total memory(Bytes)
# Should cycle time be a variable?
# No of processes?

    for c_i in range(0,100,5): # CPU limit 0-100%
        for m_i in range(0,math.ceil(memory/1024)-1,1): # Memory usage 0-memory
            for i in range(10):
                injector.CPUStress(limit=c_i) # Inject CPU stress
                if m_i>0:
                    injector.MemoryStress(gigabytes=m_i) # Inject memory stress
                cpu_util = psutil.cpu_percent()
                mem_util = psutil.virtual_memory().percent # Make it run in background when performing compression (Pending)
                cpu_freq = psutil.cpu_freq().current # Get CPU frequency in Mhz

                # Initialize variables for compression
                total_data_size = 0
                compressed_data_size = 0

                # Use a tcp packet instead
                with open(path,'rb') as input_file:
                    data = input_file.read()
                    total_data_size += len(data)
                    # compressor = zstandard.ZstdCompressor(level=compression_level)
                    
                start_time = time.time()  # Track compression time
                for chunk in compressor.read_to_iter(data,read_size = 65536*2): #default value
                    compressed_data = compressor.compress(chunk)
                compression_time = time.time() - start_time 

                compressed_data_size += len(compressed_data)
                compression_speed = total_data_size / compression_time / (1024*1024) #MB/s
                compression_ratio = total_data_size / compressed_data_size
                packet_size_diff_rate = (total_data_size - compressed_data_size) / compression_time / (1024*1024)

                print(time.strftime("%Y-%m-%d %H:%M:%S"), cpus, cpu_util, cpu_freq, memory, mem_util, compression_speed, compression_ratio, packet_size_diff_rate)
                writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), cpus, cpu_util, cpu_freq, memory, mem_util, compression_speed, compression_ratio, packet_size_diff_rate])
                time.sleep(0.1)
            
            print(f"System statistics recorded to: {output_file}")
