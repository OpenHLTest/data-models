from OpenHlTest import *
from YangBase import *
import base64
import time


openhltest = OpenHlTest('127.0.0.1', 443)

# authenticate_input = OpenHlTest.AuthenticateInput()
# authenticate_input.username = 'admin'
# authenticate_input.password = 'admin'
# openhltest.authenticate(authenticate_input)

session = openhltest.create_sessions('demo', description='Vendor prototype demo session')
session.dump()

config = session.config()
load_input = Config.LoadInput()
with open('c:/temp/demo.ixncfg', 'rb') as fid:
    load_input.vendor_config = base64.b64encode(fid.read())
config.load(load_input)
config.refresh()

connect_ports_input = Config.ConnectPortsInput()
portId = 1
for port in config.ports():
    port_map = Config.ConnectPortsInput.PortMap()
    port_map.port_name = port.name
    port_map.chassis = '10.36.74.17'
    port_map.card = 1
    port_map.port = portId
    connect_ports_input.port_map.append(port_map)
    portId += 1
errata = config.connect_ports(connect_ports_input)

start_protocols_input = Config.StartProtocolsInput()
for protocol_group in config.protocol_groups():
    start_protocols_input.protocol_group_names.append(protocol_group.name)
config.start_protocols(start_protocols_input)

start_traffic_input = Config.StartTrafficInput()
for traffic_group in config.traffic_groups():
    start_traffic_input.traffic_group_names.append(traffic_group.name)
config.start_traffic(start_traffic_input)

for i in range(0, 10):
    for port in session.statistics().ports():
        port.dump()
    time.sleep(2)

session.delete()
