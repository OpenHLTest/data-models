import sys
import os
path = os.path.realpath(__file__)
sys.path.insert(0, path[0:path.rfind('openhltest') + len('openhltest')])

from openhltest import *
from httptransport import HttpError
import base64
import time

openhltest = Openhltest('127.0.0.1', 443)

try:
    session = openhltest.create_sessions('demo')
    session.dump()
except HttpError as e:
    print(e.message)

try:
    config = session.config()
    load_input = config.LoadInput()
    with open('c:/temp/demo.ixncfg', 'rb') as fid:
        load_input.vendor_config = base64.b64encode(fid.read())
    config.load(load_input)
    config.refresh()
except HttpError as e:
    print(e.message)

try:
    connect_ports_input = config.ConnectPortsInput()
    portId = 1
    for port in config.ports():
        port_map = connect_ports_input.PortMap()
        port_map.port_name = port.name
        port_map.chassis = '10.36.74.17'
        port_map.card = 1
        port_map.port = portId
        connect_ports_input.port_map.append(port_map)
        portId += 1
    errata = config.connect_ports(connect_ports_input)
except HttpError as e:
    print(e.message)

try:
    start_protocols_input = config.StartProtocolsInput()
    for protocol_group in config.protocol_groups():
        start_protocols_input.protocol_group_names.append(protocol_group.name)
    config.start_protocols(start_protocols_input)
except HttpError as e:
    print(e.message)

try:
    start_traffic_input = config.StartTrafficInput()
    for traffic_group in config.traffic_groups():
        start_traffic_input.traffic_group_names.append(traffic_group.name)
    config.start_traffic(start_traffic_input)
except HttpError as e:
    print(e.message)

try:
    stats = session.statistics()
    for i in range(0, 10):
        for port in stats.ports():
            port.dump()
        time.sleep(2)
except HttpError as e:
    print(e.message)

try:
    session.delete()
except HttpError as e:
    print(e.message)
