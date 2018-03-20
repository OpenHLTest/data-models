import RestconfTransport
import base64

# BEGIN USER MODIFIABLE PARAMETERS
restconf_server = '127.0.0.1'
restconf_port = 443
vendor_config_filename = "c:/temp/demo.ixncfg"
session_payload = {
    'openhltest-session:sessions': {
        'name': 'demo',
        'session-type': 'L2L3'
    }
}
load_payload = {
    'openhltest-session:input': {
        'vendor-config': None
    }
}
connect_ports_payload = {
    "openhltest-session:input": [
        {
            "port-name": "Ethernet - 001",
            "chassis": "10.36.74.17",
            "card": 1,
            "port": 1
        },
        {
            "port-name": "Ethernet - 002",
            "chassis": "10.36.74.17",
            "card": 1,
            "port": 2
        }
    ]
}
start_protocols_payload = {
    "openhltest-session:input": {
        "protocol-group-names": []
    }
}
start_traffic_payload = {
    "openhltest-session:input": {
        "traffic-group-names": []
    }
}
# END USER MODIFIABLE PARAMETERS

transport = RestconfTransport.RestconfTransport(restconf_server, restconf_port)
transport.trace = True

# 1) create a session
response = transport.post('/restconf/data', payload=session_payload)
assert(response.openhltest_session_sessions.name == 'demo')

# 2) load a vendor specific configuration
with open(vendor_config_filename, 'rb') as fid:
    load_payload['openhltest-session:input']['vendor-config'] = base64.b64encode(fid.read())
    response = transport.post('/restconf/data/openhltest-session:sessions=demo/config/load', payload=load_payload)

# 3) Retrieve only read/write configuration nodes in JSON format
response = transport.get('/restconf/data/openhltest-session:sessions=demo/config?content=config')
print('Config contents:')
for port in response.openhltest_session_config.ports:
    print('\tPort: %s' % port.name)
for protocol_group in response.openhltest_session_config.protocol_groups:
    print('\tProtocol Group: %s' % protocol_group.name)
for traffic_group in response.openhltest_session_config.traffic_groups:
    print('\tTraffic Group: %s' % traffic_group.name)
    
# 4) connect abstract ports to actual hardware and/or virtual ports
response = transport.post('/restconf/data/openhltest-session:sessions=demo/config/connect-ports', payload=connect_ports_payload)

# 5) start protocols
response = transport.post('/restconf/data/openhltest-session:sessions=demo/config/start-protocols', payload=start_protocols_payload)

# 6) clear statistics
transport.post('/restconf/data/openhltest-session:sessions=demo/statistics/clear')

# 7) start traffic
response = transport.post('/restconf/data/openhltest-session:sessions=demo/config/start-traffic', payload=start_traffic_payload)

# 8) retrieve statistics
response = transport.get('/restconf/data/openhltest-session:sessions=demo/statistics')
