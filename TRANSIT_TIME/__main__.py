import subprocess
import sys

if len(sys.argv) != 4:
    print("Usage: python transittime.py community host_ip fileSize")
    sys.exit(1)

community = sys.argv[1]
host_ip = sys.argv[2]
fileSize = sys.argv[3]

main_script_args = ["python", "main.py", community, host_ip, fileSize]
result = subprocess.run(main_script_args, capture_output=True, text=True)

args =result.stdout.strip().split('\n')
stt = float(args[0])
transmissiontime =float(args[1])
routingdelay = float(args[2])

transittime = transmissiontime + stt + routingdelay
print(transittime)

