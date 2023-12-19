import psutil
import time 
import csv
import zstandard
import os
import sys
import stressinjector as injector
import resource
import math
import subprocess
import string
import random

def create_ram_disk(size_mb, mount_point):
    subprocess.run(["sudo", "mkdir", "-p", mount_point])
    subprocess.run(["sudo", "mount", "-t", "tmpfs", "-o", f"size={size_mb}M", "tmpfs", mount_point])

def clear_ram_disk(mount_point):
    # Remove all files from the RAM disk
    subprocess.run(["sudo", "rm", "-r", f"{mount_point}/*"])

def remove_ram_disk(mount_point):
    subprocess.run(["sudo", "umount", mount_point])

def write_dummy_data_to_ram_disk(mount_point, file_name):
    # Copy the filler file to the RAM disk
    subprocess.run(["sudo", "cp", file_name, mount_point])
    
output_file = 'system_stats.csv'
path = sys.argv[1]

# Run this code on different hardware specifications

with open(output_file,'a',newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Timestamp", "No of CPUs", "CPU Utilization (%)", "CPU Frequency (Mhz)", "Memory (MB)", "Memory Utilization (%)", "Compression Speed (MB/s)", "Compression Ratio", "Packet size difference rate"])

    compressor = zstandard.ZstdCompressor(level=3)

    cpus = psutil.cpu_count()# Considers logical cores also    
    memory = psutil.virtual_memory().total/(1024*1024)# Get total memory(MiB)
# Should cycle time be a variable? (Change execution cap in the vm)
# No of processes?
    for c_i in range(0,100,5): # CPU limit 0-100%
        for m_i in range(0,math.ceil(memory/1024)-1,1): # Memory usage 0-memory
                create_ram_disk(m_i*1024, "/mnt/ramdisk")

                injector.CPUStress(limit=c_i) # Inject CPU stress
                # Utilize memory
                write_dummy_data_to_ram_disk("/mnt/ramdisk", f"filler_files/dummy{m_i}.txt")
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
                clear_ram_disk("/mnt/ramdisk")
                
                compression_time = time.time() - start_time 
                compressed_data_size += len(compressed_data)
                compression_speed = total_data_size / compression_time / (1024*1024) #MB/s
                compression_ratio = total_data_size / compressed_data_size
                packet_size_diff_rate = (total_data_size - compressed_data_size) / compression_time / (1024*1024)

                print(time.strftime("%Y-%m-%d %H:%M:%S"), cpus, cpu_util, cpu_freq, memory, mem_util, compression_speed, compression_ratio, packet_size_diff_rate)
                writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), cpus, cpu_util, cpu_freq, memory, mem_util, compression_speed, compression_ratio, packet_size_diff_rate])
                time.sleep(0.1)
            
                print(f"System statistics recorded to: {output_file}")
                remove_ram_disk("/mnt/ramdisk")