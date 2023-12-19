import psutil
import os
import string
import random
def generate_dummy_data(size_kb):
    # Generate random string data
    characters = string.ascii_letters + string.digits
    data = ''.join(random.choice(characters) for _ in range(int(size_kb) * 1024))
    return data

def write_dummy_data_to_ram_disk(file_name, size_kb):
    # Write dummy data to a file in the RAM disk
    with open(file_name, "w") as file:
        dummy_data = generate_dummy_data(size_kb)
        file.write(dummy_data)

for i in range(int(psutil.virtual_memory().total/(1024*1024*1024))):
    write_dummy_data_to_ram_disk(f"filler_files/dummy{i}.txt", i*1024*1024)
# (Some problem)