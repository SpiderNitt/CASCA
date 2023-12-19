import subprocess
import sys
import concurrent.futures
from roundTripTime import rtt
from transmissionTime import calculate_transmission_time

def get_round_trip_time(host_ip):
    result = rtt(host_ip, time_interval/20, time_interval)
    return float(result) / 2

def get_bandwidth(host_ip):
    result = subprocess.run(["./bandwidth.sh", host_ip, str(time_interval)], stdout=subprocess.PIPE, text=True)
    output_lines = result.stdout.split('\n')
    return int(output_lines[0].rstrip('Mbits/sec').strip())

def get_transmission_time(file_size, bandwidth):
    result = calculate_transmission_time(float(file_size), float(bandwidth))
    return float(result)

def get_routing_delay(community, host_ip):
    
    routing_delay_args = ["python", "routingDelay/", community, host_ip, "routingDelay/", str(time_interval)]
    result = subprocess.run(routing_delay_args, capture_output=True, text=True)
    return float(result.stdout.strip())

def get_vals(community, host_ip, file_size):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        rtt_future = executor.submit(get_round_trip_time, host_ip)
        bandwidth_future = executor.submit(get_bandwidth, host_ip)
        transmission_time_future = executor.submit(get_transmission_time, file_size, bandwidth_future.result())
        routing_delay_future = executor.submit(get_routing_delay, community, host_ip)

        round_trip_time = rtt_future.result()
        single_trip_time = round_trip_time / 2
        print(f"Single-Trip Time: {single_trip_time:.4f}")

        transmission_time = transmission_time_future.result()
        print(f"Transmission Time: {transmission_time}")

        routing_delay = routing_delay_future.result()
        print(f"Routing Delay: {routing_delay}")
        routing_delay = 0

        transit_time = single_trip_time + transmission_time + routing_delay
        print(f"Total Transit time : {transit_time}")

if len(sys.argv) != 5:
    print("python transittime community host_ip file_size time_interval")
    sys.exit(1)

community = sys.argv[1]
host_ip = sys.argv[2] 
file_size = sys.argv[3] 
time_interval = float(sys.argv[4]) 

get_vals(community, host_ip, file_size)

