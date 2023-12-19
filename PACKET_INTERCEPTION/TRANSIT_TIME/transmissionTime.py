import subprocess
import sys


def calculate_transmission_time(packet_length, bandwidth):
    packet_length_bits = packet_length * 8

    transmission_time = packet_length_bits / (bandwidth * 10**6) 

    return transmission_time

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python transmission_time.py packet_length bandwidth")
        sys.exit(1)

    packet_length = int(sys.argv[1])
    bandwidth = int(sys.argv[2])

    transmission_time = calculate_transmission_time(packet_length, bandwidth)
    print(f"{transmission_time:.6f}")

