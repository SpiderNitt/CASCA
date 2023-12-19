import time
from concurrent.futures import ThreadPoolExecutor
from ping3 import ping, verbose_ping
import sys

def measure_latency(target, interval, duration):
    results = []

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(ping, target): _ for _ in range(int(duration / interval))}

        for future in futures:
            try:
                result = future.result()
                if result is not None:
                    results.append(result)
            except Exception as e:
                print(f"An error occurred: {e}")

    return results

def calculate_average_rtt(results):
    if not results:
        return None
    return sum(results) / len(results)

def rtt(target_host, ping_interval, measurement_duration):


    latency_results = measure_latency(target_host, ping_interval, measurement_duration)

    avg_rtt = calculate_average_rtt(latency_results)
    return(f"{avg_rtt:.4f}")

if __name__ == "__main__":
    rtt()

