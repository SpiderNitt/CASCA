import subprocess
import sys
import concurrent.futures
from roundTripTime import rtt
from transmissionTime import calculate_transmission_time

def get_round_trip_time(host_ip):
    result = rtt(host_ip, time_interval/20, time_interval)
    return float(result) 

def get_bandwidth(host_ip):
    result = subprocess.run(["./bandwidth.sh", host_ip, str(time_interval)], stdout=subprocess.PIPE, text=True)
    output_lines = result.stdout.split('\n')
    print(output_lines[0])
    return int(output_lines[0].rstrip('Mbits/sec').strip())

def get_transmission_time(file_size, bandwidth):
    result = calculate_transmission_time(float(file_size), float(bandwidth))
    return float(result)


def get_vals(file_size, host_ip):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        rtt_future = executor.submit(get_round_trip_time, host_ip)
        bandwidth_future = executor.submit(get_bandwidth, host_ip)
        transmission_time_future = executor.submit(get_transmission_time, file_size, bandwidth_future.result())


        round_trip_time = rtt_future.result()
        single_trip_time = round_trip_time / 2
        print(single_trip_time)

        transmission_time = transmission_time_future.result()


        transit_time = single_trip_time + transmission_time 
        print(f"{transit_time:.6f}")

if len(sys.argv) != 4:
    print("python transittime file_size time_interval host_ip")
    sys.exit(1)

file_size = sys.argv[1] 
time_interval = float(sys.argv[2]) 
host_ip = sys.argv[3]

get_vals( file_size, host_ip)

