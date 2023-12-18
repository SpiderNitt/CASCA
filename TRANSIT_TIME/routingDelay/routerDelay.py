from pysnmp.hlapi import *
import sys
import time

def get_snmp_metric(oid, community, device_ip):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((device_ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )

    if errorIndication:
        print(f"SNMP Error: {errorIndication}")
        return None
    else:
        return int(varBinds[0][1])

def estimate_queuing_delay(community, device_ip, time_interval, interface_index):

    base_oid = '1.3.6.1.2.1.2.2.1'

    ifInOctets_oid = f'{base_oid}.10.{interface_index}'
    ifOutOctets_oid = f'{base_oid}.16.{interface_index}'
    ifInDiscards_oid = f'{base_oid}.13.{interface_index}'
    ifOutDiscards_oid = f'{base_oid}.19.{interface_index}'

    current_ifInOctets = get_snmp_metric(ifInOctets_oid, community, device_ip)
    current_ifOutOctets = get_snmp_metric(ifOutOctets_oid, community, device_ip)
    current_ifInDiscards = get_snmp_metric(ifInDiscards_oid, community, device_ip)
    current_ifOutDiscards = get_snmp_metric(ifOutDiscards_oid, community, device_ip)

    # Sleep for the specified time interval
    time.sleep(time_interval)

    # Get previous SNMP metrics
    previous_ifInOctets = get_snmp_metric(ifInOctets_oid, community, device_ip)
    previous_ifOutOctets = get_snmp_metric(ifOutOctets_oid, community, device_ip)
    previous_ifInDiscards = get_snmp_metric(ifInDiscards_oid, community, device_ip)
    previous_ifOutDiscards = get_snmp_metric(ifOutDiscards_oid, community, device_ip)

    # Calculate rates and estimate queuing delay
    input_rate = (current_ifInOctets - previous_ifInOctets) / time_interval
    output_rate = (current_ifOutOctets - previous_ifOutOctets) / time_interval
    in_discard_rate = (current_ifInDiscards - previous_ifInDiscards) / time_interval
    out_discard_rate = (current_ifOutDiscards - previous_ifOutDiscards) / time_interval

    if (input_rate + output_rate > 0):
        queuing_delay_estimate = (in_discard_rate + out_discard_rate) / (input_rate + output_rate)
    else:
        queuing_delay_estimate = 0

    print(queuing_delay_estimate)

if len(sys.argv) != 5:
    print("Usage: python routerDelay.py community_string router_ip_addr time_interval_sec interface_index")
    sys.exit(1)

community_string = sys.argv[1]
router_ip_address = sys.argv[2]
time_interval_seconds = int(sys.argv[3])
interface_index = int(sys.argv[4])

estimate_queuing_delay(community_string, router_ip_address, time_interval_seconds, interface_index)

