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
```

### PROPOSED GENERATED CODE
```python
from HttpTransport import HttpTransport
from YangBase import YangBase


class ConfigPorts(YangBase):
    '''Description from yang model goes here'''
    def __init__(self, parent, yang_key_value=None):
        self.YANG_MODULE = 'openhltest-session'
        self.YANG_CLASS = 'ports'
        self.YANG_KEY = 'name'
        super(ConfigPorts, self).__init__(parent, yang_key_value)

    @property
    def name(self):
        return self._get_value('name')

class ConfigProtocolGroups(YangBase):
    '''Description from yang model goes here'''
    def __init__(self, parent, yang_key_value=None):
        self.YANG_MODULE = 'openhltest-session'
        self.YANG_CLASS = 'protocol-groups'
        self.YANG_KEY = 'name'
        super(ConfigProtocolGroups, self).__init__(parent, yang_key_value)

    @property
    def name(self):
        '''Description from yang model goes here'''
        return self._get_value('name')

class ConfigTrafficGroups(YangBase):
    '''Description from yang model goes here'''
    def __init__(self, parent, yang_key_value=None):
        self.YANG_MODULE = 'openhltest-session'
        self.YANG_CLASS = 'traffic-groups'
        self.YANG_KEY = 'name'
        super(ConfigTrafficGroups, self).__init__(parent, yang_key_value)

    @property
    def name(self):
        '''Description from yang model goes here'''
        return self._get_value('name')

class StatisticsPorts(YangBase):
    '''Description from yang model goes here'''
    def __init__(self, parent, yang_key_value=None):
        self.YANG_MODULE = 'openhltest-session'
        self.YANG_CLASS = 'ports'
        self.YANG_KEY = 'name'
        super(StatisticsPorts, self).__init__(parent, yang_key_value)

    @property
    def name(self):
        '''Description from yang model goes here'''
        return self._get_value('name')
    
    @property
    def connected_test_port_id(self):
        '''Description from yang model goes here'''
        return self._get_value('connected-test-port-id')

    @property
    def connected_test_port_description(self):
        '''Description from yang model goes here'''
        return self._get_value('connected-test-port-description')

    @property
    def connection_state(self):
        '''Description from yang model goes here'''
        return self._get_value('connection-state')

    @property
    def connection_state_details(self):
        '''Description from yang model goes here'''
        return self._get_value('connection-state-details')

    @property
    def speed(self):
        '''Description from yang model goes here'''
        return self._get_value('speed')

    @property
    def tx_frames(self):
        '''Description from yang model goes here'''
        return self._get_value('tx-frames')

    @property
    def rx_frames(self):
        '''Description from yang model goes here'''
        return self._get_value('rx-frames')


class Config(YangBase):
    '''Description from yang model goes here'''
    def __init__(self, parent, yang_key_value=None):
        self.YANG_MODULE = 'openhltest-session'
        self.YANG_CLASS = 'config'
        super(Config, self).__init__(parent, yang_key_value)

    @property
    def description(self):
        '''Getter Description from yang model goes here'''
        return self._get_value('description')
    @description.setter
    def description(self, value):
        '''Setter Description from yang model goes here'''
        self._set_value('description', value)
        
    def ports(self, name=None):
        return self._read(ConfigPorts(self, name))

    def create_ports(self, name, description=None):
        return self._create(self, ConfigPorts(self, name), locals())

    def protocol_groups(self, name=None):
        return self._read(ConfigProtocolGroups(self, name))

    def traffic_groups(self, name=None):
        return self._read(ConfigTrafficGroups(self, name))

    class LoadInput(object):
        def __init__(self):
            self.YANG_PATH = 'openhltest-session:input'
            self.vendor_config = ''

    def load(self, load_input):
        '''Action should be current object's url + "/<action name>'''
        return self._execute(self.url + '/load', load_input)

    class ConnectPortsInput(object):
        def __init__(self, port_map=[]):
            self.YANG_PATH = 'openhltest-session:input'
            self.port_map = port_map

        class PortMap(object):
            def __init__(self, port_name='', chassis='', card=0, port=0):
                self.port_name = port_name
                self.chassis = chassis
                self.card = card
                self.port = port

    class ConnectPortsOutput(object):
        '''Description from yang model goes here'''
        def __init__(self, errata=[]):
            self.YANG_PATH = 'openhltest-session:output'
            self.errata = errata

        class Errata(object):
            '''Description from yang model goes here'''
            def __init__(self, name='', detail='', stack_trace=''):
                self.name = name
                self.detail = detail
                self.stack_trace = stack_trace
        
    def connect_ports(self, connect_ports_input):
        '''Action should be current object's url + "/<action name>'''
        return self._execute(self.url + '/connect-ports', connect_ports_input, Config.ConnectPortsOutput())

    class StartProtocolsInput(object):
        def __init__(self):
            self.YANG_PATH = 'openhltest-session:input'
            self.protocol_group_names = []

    def start_protocols(self, start_protocols_input):
        '''Action should be current object's url + "/<action name>'''
        return self._execute(self.url + '/start-protocols', start_protocols_input)

    class StartTrafficInput(object):
        def __init__(self):
            self.YANG_PATH = 'openhltest-session:input'
            self.traffic_group_names = []

    def start_traffic(self, start_traffic_input):
        '''Action should be current object's url + "/<action name>'''
        return self._execute(self.url + '/start-traffic', start_traffic_input)


class Statistics(YangBase):
    '''Description from yang model goes here'''
    def __init__(self, parent, yang_key_value=None):
        self.YANG_MODULE = 'openhltest-session'
        self.YANG_CLASS = 'statistics'
        super(Statistics, self).__init__(parent, yang_key_value)

    @property
    def last_activity_timestamp(self):
        return self._get_value('last-activity-timestamp')

    @property
    def first_activity_timestamp(self):
        return self._get_value('first-activity-timestamp')

    def ports(self, name=None):
        return self._read(StatisticsPorts(self, name))
    

class Sessions(YangBase):
    '''Description from yang model goes here'''
    def __init__(self, parent, yang_key_value=None):
        self.YANG_MODULE = 'openhltest-session'
        self.YANG_CLASS = 'sessions'
        self.YANG_KEY = 'name'
        super(Sessions, self).__init__(parent, yang_key_value)
    
    @property
    def name(self):
        '''Description from yang model goes here'''
        return self._get_value('name')

    @property
    def session_type(self):
        '''Description from yang model goes here'''
        return self._get_value('session-type')

    def update(self):
        '''Updates the current object with any changes made using property setters'''
        return self._update()
    
    def delete(self):
        '''Deletes the current object'''
        return self._delete()

    def config(self):
        '''Description from yang model goes here'''
        return self._read(Config(self))

    def statistics(self):
        '''Description from yang model goes here'''
        return self._read(Statistics(self))


class OpenHlTest(YangBase):
    '''Description from yang model goes here'''

    def __init__(self, ip_address, rest_port):
        self.YANG_MODULE = ''
        self.YANG_CLASS = ''
        super(OpenHlTest, self).__init__(HttpTransport(ip_address, rest_port), None)

    def sessions(self, name=None):
        '''Description from yang model goes here'''
        return self._read(Sessions(self, name))

    def create_sessions(self, name, session_type='L2L3', description=None):
        '''Description from yang model goes here'''
        return self._create(Sessions(self, name), locals())

    class AuthenticateInput:
        '''Description from yang model goes here'''
        def __init__(self):
            self.YANG_PATH = 'openhltest-session:input'
            self.username = ''
            self.password = ''

    def authenticate(self, authenticate_input):
        '''RPC should be the entire url - /restconf/operations/<modulename>:<rpc name>'''
        #return self._execute('/restconf/operations/openhltest-session:authenticate', authenticate_input)
        return None
```
