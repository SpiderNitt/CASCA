
from subprocess import run
import sys

if len(sys.argv) != 5 :
    print("python routerDelay community host_ip path time_interval")
    sys.exit(1)

community = sys.argv[1]
host_ip = sys.argv[2]
path = sys.argv[3]
time_interval = sys.argv[4]

interface_index_arguments = ["python", path+"interface_index.py", community, host_ip]
interface_index_result = run(interface_index_arguments, capture_output=True, text=True)
interface_index = interface_index_result.stdout.strip()  


routing_delay_arguments = ["python", path+"routerDelay.py", community, host_ip, str(time_interval), interface_index]
routing_delay_result = run(routing_delay_arguments, capture_output=True, text=True)
routing_delay = routing_delay_result.stdout.strip()

print(routing_delay)
