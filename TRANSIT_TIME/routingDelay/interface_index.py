from pysnmp.hlapi import *
import sys

if len(sys.argv) != 3:
    print("python testRouter.py community router_ip")
    sys.exit(1)

community = sys.argv[1]
router_ip = sys.argv[2]

ifIndex_OID = ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.1'))

def snmp_walk(oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        bulkCmd(SnmpEngine(),
                CommunityData(community),
                UdpTransportTarget((router_ip, 161)),
                ContextData(),
                0, 25,  # Non-repeaters and max-repetitions
                oid)
    )

    if errorIndication:
        print(f"SNMP Error: {errorIndication}")
        return None
    elif errorStatus:
        print(f"SNMP Error: {errorStatus.prettyPrint()}")
        return None
    else:
        interface_indexes = [int(varBind[0][-1]) for varBind in varBinds]
        return interface_indexes

interface_indexes = snmp_walk(ifIndex_OID)

if interface_indexes is not None:
    print(interface_indexes[0])

