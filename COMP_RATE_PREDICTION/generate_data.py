import psutil
import time 
import csv
import zstandard
import os

output_file = 'system_stats.csv'
interval = 1 #1sec
path = '/home/pratyush/Desktop/Networks/data' #change your data path
with open(output_file,'w',newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Timestamp", "CPU Utilization (%)", "Memory Utilization (%)", "Compression Speed (MB/s)"])
    compressor = zstandard.ZstdCompressor(level=3)
    for i in range(100):
        start_time = time.time()  # Track compression time

        # Get CPU and memory utilization
        cpu_util = psutil.cpu_percent()
        mem_util = psutil.virtual_memory().percent

        # Initialize variables for compression
        total_data_size = 0
        compressed_data_size = 0

        for j in os.listdir(path):
            with open(os.path.join(path,j),'rb') as input_file:
                data = input_file.read()
                total_data_size += len(data)
            # compressor = zstandard.ZstdCompressor(level=compression_level)
            

        for chunk in compressor.read_to_iter(data,read_size = 65536*2): #default value
            compressed_data = compressor.compress(chunk)
        compressed_data_size += len(compressed_data)
        compression_time = time.time() - start_time
        compression_speed = total_data_size / compression_time / 1048576 #MB/s
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), cpu_util, mem_util, compression_speed])
        time.sleep(interval)
    
    print(f"System statistics recorded to: {output_file}")
