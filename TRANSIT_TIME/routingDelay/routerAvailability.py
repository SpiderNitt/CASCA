from pysnmp.hlapi import *
import sys

if len(sys.argv) != 3 :
    print("python testRouter.py community router_ip")
    sys.exit(1)

community = sys.argv[1] 
router_ip = sys.argv[2]

sysUpTime_OID = ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0'))  # System Uptime
ifOperStatus_OID = ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.8.1'))  # Interface Operational Status
ifInQueue_OID = ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.21.1'))  # Input Queue Length

def snmp_get(oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((router_ip, 161)),
               ContextData(),
               oid)
    )

    if errorIndication:
        return None
    else:
        print(f"Result: {varBinds[0][1].prettyPrint()}")

sys_uptime = snmp_get(sysUpTime_OID)
print(f"System Uptime: {sys_uptime}")

if_oper_status = snmp_get(ifOperStatus_OID)
print(f"Interface Operational Status: {if_oper_status}")

input_queue_length = snmp_get(ifInQueue_OID)
print(f"Input Queue Length: {input_queue_length}")

