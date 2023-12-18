import subprocess
import sys

def getvals(community, host_ip, fileSize) :
    result = subprocess.run(["./network.sh", host_ip], stdout=subprocess.PIPE, text=True)
    output_lines = result.stdout.split('\n')

    singleTripTime = str(float(output_lines[1].strip())/2)
    bandwidth = str(int(output_lines[0].rstrip('Mbits/sec').strip()))
    
    transmissionTimeArgs = ["python", "transmissionTime.py", fileSize, bandwidth]
    transTime = subprocess.run(transmissionTimeArgs, capture_output=True, text=True)
    transmissionTime = transTime.stdout.strip()
    
    print(singleTripTime)
    print(transmissionTime)

    routingDelayArgs = ["python", "routingDelay/", community, host_ip ,"routingDelay/"]
    routingDel = subprocess.run(routingDelayArgs, capture_output=True, text=True)
    routingDelay = routingDel.stdout.strip()

    print(routingDelay)

if len(sys.argv) != 4 :
    print("python transittime community host_ip fileSize")
    sys.exit(1)

community = sys.argv[1]
host_ip = sys.argv[2]
fileSize = sys.argv[3]

getvals(community, host_ip, fileSize)
