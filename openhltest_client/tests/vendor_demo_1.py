'''A vendor demo scaffolding script that demonstrates the following:

Configures the test tool with the following:
    2 ports connected back to back
    2 device-groups each with one port
        1 device with the following protocols:
            ethernet
            vlan
            ipv4
            bgpv4
        1 simulated network
            1 network of type bgpv4 route range
    1 device-traffic from one bgpv4 route range to the other

Connects ports to test hardware
Starts device-groups
Clears statistics
Starts device-traffic
Stops device-traffic
Displays port statistics
Displays device-traffic statistics

'''
import json
import time
from openhltest_client.httptransport import HttpTransport


OPENHLTEST_SERVER = '127.0.0.1:443'
SESSION_NAME = 'IxNetwork GUI'
CONFIG = [
    {
        'location': '10.36.74.26/2/13',
        'ipv4': {
            "source-address": '1.1.1.1',
            'prefix': 24,
            'gateway-address': '1.1.1.2'
        },
        'bgpv4': {
            'dut-ipv4-address': '1.1.1.2'
        } 
    },
    {
        'location': '10.36.74.26/2/14',
        'ipv4': {
            "source-address": '1.1.1.2',
            'prefix': 24,
            'gateway-address': '1.1.1.1'
        },
        'bgpv4': {
            'dut-ipv4-address': '1.1.1.1'
        }
    }
]
CONFIG_FILENAME = "./config.json"


transport = HttpTransport(OPENHLTEST_SERVER)
# transport.set_debug_level()

transport.info('get an instance of the OpenHlTest module class')
openhltest = transport.OpenHlTest

transport.info('get a Sessions instance')
sessions = None
try:
    sessions = openhltest.Sessions.read()
except Exception as e:
    transport.info(e)
if sessions is None or len(sessions) == 0:
    sessions = openhltest.Sessions.create(SESSION_NAME)
transport.info(sessions)

transport.info('get an instance of the Config class and clear the configuration')
config = sessions.Config
config.Clear()

networks = []
for i in range(0, len(CONFIG)):
    port = config.Ports.create(Name='Port_%s' % (i + 1), Location=CONFIG[i]['location'])
    transport.info('add port %s' % port.Name)

    transport.info('add %s bgp protocol scenario' % port.Name)
    device_group = config.DeviceGroups.create(Name='Device_Group_%s' % port.Name, Ports=port)
    device = device_group.Devices.create(Name='Device_%s' % port.Name , DeviceCountPerPort=1, ParentLink=None)
    parent = None
    for protocol_type in ['ETHERNET', 'VLAN', 'IPV4', 'BGPV4']:
        protocol = device.Protocols.create(Name='%s_%s' % (protocol_type, port.Name), ProtocolType=protocol_type, ParentLink=parent)
        if protocol_type == 'IPV4':
            protocol.Ipv4.SourceAddress.update(PatternType='SINGLE', Single=CONFIG[i]['ipv4']['source-address'])
            protocol.Ipv4.Prefix.update(PatternType='SINGLE', Single=CONFIG[i]['ipv4']['prefix'])
            protocol.Ipv4.GatewayAddress.update(PatternType='SINGLE', Single=CONFIG[i]['ipv4']['gateway-address'])
        elif protocol_type == 'BGPV4':
            protocol.Bgpv4.DutIpv4Address.update(PatternType='SINGLE', Single=CONFIG[i]['bgpv4']['dut-ipv4-address'])
        parent = protocol.Name

    transport.info('add %s bgp route range' % device.Name)
    simulated_network = device_group.SimulatedNetworks.create(Name='Simulated_Network_%s' % port.Name, ParentLink=device.Name)
    network = simulated_network.Networks.create(Name='Network_%s' % port.Name, NetworkType='BGPV4_ROUTE_RANGE', NetworkCountPerPort=5, FlowLink='BGPV4_%s' % port.Name)
    network.Bgpv4RouteRange.Address.update(PatternType='SINGLE', Single='10.10.10.1')
    network.Bgpv4RouteRange.AsPath.update(PatternType='SINGLE', Single='20')
    network.Bgpv4RouteRange.PrefixLength.update(PatternType='SINGLE', Single='16')
    networks.append(network)

traffic = config.DeviceTraffic.create(Name='Device_Traffic', Encapsulation='IPV4', BiDirectional=True, MeshType='ONE_TO_ONE', Sources=networks[0], Destinations=networks[1])
transport.info('added %s' % traffic.Name)
tcp = traffic.Frames.create(Name='TCP', FrameType='TCP').Tcp
tcp.SourcePort.update(PatternType='SINGLE', Single='12345')
tcp.DestinationPort.update(PatternType='SINGLE', Single='54321')

transport.info('configure frame length')
traffic.FrameLength.update(LengthType='INCREMENT').Increment.update(Start=68, End=1024, Step=2)

transport.info('configure frame rate')
traffic.FrameRate.update(Mode='FIXED').FixedRate.update(RateType='FRAMES_PER_SECOND', Fps=1024)
config.Commit()

transport.info('connect all ports')
config.PortControl({"mode": "CONNECT", "targets": []})

transport.info("start the device-groups")
config.DeviceGroupsControl({"mode": "START", "targets": []})

transport.info('clear statistics')
sessions.Statistics.Clear()

transport.info('start traffic')
config.TrafficControl({"mode": "START", "targets": []})

time.sleep(5)

transport.info('stop traffic')
config.TrafficControl({"mode": "STOP", "targets": []})

transport.info('wait for aggregate tx rate to go to 0')
while True:
    time.sleep(1)
    tx_rate = 0
    for port in sessions.Statistics.Port.read():
        tx_rate += int(port.TxFrameRate)
    if tx_rate == 0:
        break

transport.info("port statistics")
for port in sessions.Statistics.Port.read():
    transport.info(port)

transport.info("device-traffic statistics")
for traffic in sessions.Statistics.DeviceTraffic.read():
    transport.info(traffic)

transport.info('retrieve the current configuration')
config.Save({'mode': 'RESTCONF_JSON', 'file-name': CONFIG_FILENAME})
with open(CONFIG_FILENAME) as fid:
    json_config = fid.read()
    transport.info(json_config)

transport.info('PASS')
