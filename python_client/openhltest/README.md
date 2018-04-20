# OpenHlTest yang model generated python client
This folder will act as the repository for the OpenHlTest python client module.

## Proposal
The library will follow these guidelines:
1) It will be auto-generated every time there is a model change that has been successfully validated.
2) It will be hierarchical and match the hierarchy of the yang model.
3) It will consist of base infrastructure that encapsulates transport and serialization.
4) Once the library has been generated and unit tests pass it will be packaged and posted on pypi.python.org.  
   - it will be available for install using pip install openhltest


Base infrastructure that is not auto-generated:
1) Https transport class named HttpTransport
2) Crudx and utility methods encapsulated in YangBase  
   - dump method
   - convert python dict objects to openhltest input/output objects
   - convert openhltest input/output objects to python dict objects 

The pyang plugin python_client_plugin.py will generate the following:
1) classes for the following yang keywords:  
   - container
   - list
   - input
   - output
2) class @property accessors for the following yang keywords: 
   - leaf
   - leaf-list
3) class methods for the following yang keywords:  
   - action
   - rpc
4) class @property accessors to access child container, list classes
5) class create_... methods to create child list siblings (only rw list keyword)  
   - rw list will have the yang key as a required parameter
   - all other leaf, leaf-list keywords will be defaulted to None if keyword default is not present
6) class update method to allow for updating dirty properties
7) class delete method to allow for deletion (only rw list keyword)
8) class dump method


### SAMPLE IMPLEMENTATION CODE 
```python
from OpenHlTest import *
from YangBase import *
import base64
import time


openhltest = OpenHlTest('127.0.0.1', 443)

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
```