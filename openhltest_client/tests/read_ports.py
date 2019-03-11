""" The following is a sanity sample

"""
from openhltest_client.httptransport import HttpTransport


# everything starts from the transport
# create an instance of the transport class
transport = HttpTransport()
transport.set_debug_level()

# get an instance of the OpenHlTest module class
openhltest = transport.OpenHlTest

# create an instance of the Sessions class
session_name = 'Test Sessions 1'
session = openhltest.Sessions.create(Name=session_name)
assert(session.Name == session_name)
print(session)

# get an instance of the Config class
config = session.Config
print(config)

# create an instance of the Ports classm add some resources and retrieve them all
for i in range(4):
	port_name = 'Test Port %s' % i
	port = config.Ports.create(Name=port_name, Location='0.0.0.%s/1/%s' % (i, i))
	assert(port.Name == port_name)
ports = config.Ports.read()
print(ports)

# create an instance of the DeviceGroups class
device_group_name = 'Device Group 1'
device_group = config.DeviceGroups.create(Name=device_group_name, Ports=ports)
assert(device_group.Name == device_group_name)
print(device_group)

# create an instance of the Devices class
device_name = 'Device 1'
device = device_group.Devices.create(Name=device_name, DeviceCountPerPort=6)
assert(device.Name == device_name)
print(device)

# create an instance of the Protocols class
protocol_name = 'Protocol 1'
protocol = device.Protocols.create(Name=protocol_name, ProtocolType='ETHERNET')
assert(protocol.Name == protocol_name)
print(protocol)

# update the Ethernet Mac pattern to increment and set the start and step values
protocol.Ethernet.Mac.update(PatternType='INCREMENT').Increment.update(Start='00:00:01:00:00:01', Step='00:00:00:00:00:01')
assert(protocol.Ethernet.Mac.Increment.Start == '00:00:01:00:00:01')
assert(protocol.Ethernet.Mac.Increment.Step == '00:00:00:00:00:01')

# start all the protocols
config.PortControl({'targets': ports, 'mode': 'START'})

# delete the protocols resource
protocol.delete()

# delete the resources encapsulated in the ports object
ports.delete()
